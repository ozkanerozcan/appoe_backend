from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter

from tasks.models import Group, List, Comment, Post, Attachment
from tasks.serializers import (
    ListReadSerializer,
    ListWriteSerializer,
    GroupSerializer,
    CommentSerializer,
    AttachmentReadSerializer,
    AttachmentWriteSerializer,
    PostReadSerializer,
    PostWriteSerializer,
    TaskDocumentSerializer,
)

from .permissions import IsAuthorOrReadOnly

from elasticsearch_dsl.query import MultiMatch
from elasticsearch_dsl import Q

from rest_framework.pagination import LimitOffsetPagination
from django.http import HttpResponse

from .documents import TaskDocument




class TaskDocumentView(APIView, LimitOffsetPagination):
    search_serializer = TaskDocumentSerializer
    search_document = TaskDocument
    '''
    def post(self, request):
        try:
            data_search = request.data.get('search')
            data_list = request.data.get('list')

            # Initialize Q object
            q_object = Q("terms", list__title=data_list)



            search = self.search_document.search().query(q_object)
            response = search.execute()
            results = self.paginate_queryset(response, request, view=self)
            serializer = self.search_serializer(results, many=True)
            print(serializer.data)
            return self.get_paginated_response(serializer.data)
        except Exception as e:
            return HttpResponse(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    '''
    
    def post(self, request):
        try:
            data = request.data
            data_search = data.get('search')
            data_dateRangeFrom = data.get('dateRangeFrom')
            data_dateRangeTo = data.get('dateRangeTo')
            data_list = data.get('list')
            data_createdBy = data.get('createdBy')
            data_status = data.get('status')
            data_workedOn = data.get('workedOn')
            print(data_list)
            '''
            # Initialize Q object
            q_object = Q()

            if data_search:
                q_object &= Q('multi-match', query=data_search, fields=['title', 'body'], fuzziness='auto')
            if data_list:
                q_object &= Q(list_title__in=data_list)
            if data_status:
                q_object &= Q(status__in=data_status)
            if data_dateRangeFrom:
                q_object &= Q(deadline_at__gte=data_dateRangeFrom)
            if data_dateRangeTo:
                q_object &= Q(deadline_at__lte=data_dateRangeTo)
            '''

            #q_object = Q('multi_match', query=data_search, fields=['list.title',], fuzziness='auto')
            '''
            q_object =  {
                        "bool": {
                            "must": [
                                {"multi_match": {
                                    "query": data_search,
                                    "fields": ["title", "body"],
                                    "fuzziness": "auto"
                                    }
                                },
                            ],
                            "filter": [
                                {"terms": {"list.title": ["6736 TEFAŞ", "Test"]}},
                            ],
                        }
                    }
            '''
            query_body = {
                    "bool": {
                        "must": [],
                        "filter": [],
                        "should": [],
                        "must_not": []
                    }
                }

            # Add a fuzzy match for the search term if provided
            if data_search:
                multi_match = {
                    "multi_match": {
                        "query": data_search,
                        "fields": ["title", "body"],
                        "fuzziness": "AUTO"
                    }
                }
                query_body["bool"]["must"].append(multi_match)

            filters = {}
            if data_list:
                filters['list.title'] = data_list
            if data_createdBy:
                filters['created_by.username'] = data_createdBy
            if data_status:
                filters['status'] = data_status
            if data_workedOn:
                filters['worked_on'] = data_workedOn


            # Add filters if provided
            if filters:
                for field, value in filters.items():
                    filter_clause = {
                        "terms": {
                            field: value
                        }
                    }
                    query_body["bool"]["filter"].append(filter_clause)

            # Add date range filter if provided
            if data_dateRangeFrom:
                date_from_filter = {
                    "range": {
                        "deadline_at": {
                            "gte": data_dateRangeFrom,
                        }
                    }
                }
                query_body["bool"]["filter"].append(date_from_filter)
            
            if data_dateRangeTo:
                date_to_filter = {
                    "range": {
                        "deadline_at": {
                            "lte": data_dateRangeTo
                        }
                    }
                }
                query_body["bool"]["filter"].append(date_to_filter)

            print(query_body)

                
            sort_param = {"deadline_at": {"order": "asc"}}
            
            #search = self.search_document.search().query(q_object)
            search = self.search_document.search().query(query_body).sort(sort_param)
            total = search.count()
            search = search[0:total]
            response = search.execute()
            results = self.paginate_queryset(response, request, view=self)
            serializer = self.search_serializer(results, many=True)
            print(serializer.data)
            return self.get_paginated_response(serializer.data)
        except Exception as e:
            return HttpResponse(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


'''
class SearchResultsList(APIView):
    """
    Search Result
    """
    
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        q = self.request.GET.get('q', "")
        #query = MultiMatch(query=q, fields=["created_by.full_name", "list.title", "list.group.title", "title", "body", ], fuzziness="AUTO")
        query = MultiMatch(query=q, fields=["title", "body", ], fuzziness="AUTO")
        
        if q == "":
            search_results = Post.objects.none()
        else:
            search_results = TaskPostDocument.search().query("match", list__title="6736 TEFAŞ").query(query).to_queryset()
        serializer = PostReadSerializer(search_results, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
'''

class PostViewSet(viewsets.ModelViewSet):
    """
    CRUD posts
    """

    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return PostWriteSerializer

        return PostReadSerializer

    def get_permissions(self):
        if self.action in ("create",):
            self.permission_classes = (permissions.IsAuthenticated,)
        elif self.action in ("update", "partial_update", "destroy"):
            self.permission_classes = (IsAuthorOrReadOnly,)
        else:
            self.permission_classes = (permissions.AllowAny,)

        return super().get_permissions()



class CommentViewSet(viewsets.ModelViewSet):
    """
    CRUD comments for a particular post
    """

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ['title', 'body']


    def perform_create(self, serializer):
        created_by = self.request.user
        serializer.save(created_by=created_by)

class GroupViewSet(viewsets.ModelViewSet):
    """
    CRUD groups
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ['title', 'body']


    def perform_create(self, serializer):
        created_by = self.request.user
        serializer.save(created_by=created_by)

class ListViewSet(viewsets.ModelViewSet):
    """
    CRUD lists
    """

    queryset = List.objects.all()

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return ListWriteSerializer

        return ListReadSerializer

    def get_permissions(self):
        if self.action in ("create",):
            self.permission_classes = (permissions.IsAuthenticated,)
        elif self.action in ("update", "partial_update", "destroy"):
            self.permission_classes = (IsAuthorOrReadOnly,)
        else:
            self.permission_classes = (permissions.AllowAny,)

        return super().get_permissions()


class AttachmentViewSet(viewsets.ModelViewSet):
    """
    CRUD attachments for a particular post
    """

    queryset = Attachment.objects.all()

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return AttachmentWriteSerializer

        return AttachmentReadSerializer

    def get_permissions(self):
        if self.action in ("create",):
            self.permission_classes = (permissions.IsAuthenticated,)
        elif self.action in ("update", "partial_update", "destroy"):
            self.permission_classes = (IsAuthorOrReadOnly,)
        else:
            self.permission_classes = (permissions.AllowAny,)

        return super().get_permissions()


class LikePostAPIView(APIView):
    """
    Like, Dislike a post
    """

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        user = request.user
        post = get_object_or_404(Post, pk=pk)

        if user in post.likes.all():
            post.likes.remove(user)

        else:
            post.likes.add(user)

        return Response(status=status.HTTP_200_OK)




from .models import Subscription
from pywebpush import webpush, WebPushException
from django.conf import settings

class Subscribe(APIView):
    def post(self, request):
        subscription_data = request.data.get('subscription')
        subscription = Subscription.objects.create(
            endpoint=subscription_data['endpoint'],
            p256dh=subscription_data['keys']['p256dh'],
            auth=subscription_data['keys']['auth']
        )
        return Response(status=201)
    
class Notify(APIView):
    def post(self, request):
        message = request.data.get('message')
        subscriptions = Subscription.objects.all()

        for sub in subscriptions:
            try:
                webpush(
                    subscription_info={
                        "endpoint": sub.endpoint,
                        "keys": {
                            "p256dh": sub.p256dh,
                            "auth": sub.auth
                        }
                    },
                    data=message,
                    vapid_private_key=settings.VAPID_PRIVATE_KEY,
                    vapid_claims=settings.VAPID_CLAIMS
                )
            except WebPushException as ex:
                print(f"Failed to send notification: {ex}")

        return Response(status=200)