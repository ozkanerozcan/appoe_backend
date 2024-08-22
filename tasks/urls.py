from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import GroupViewSet, ListViewSet, CommentViewSet, PostViewSet, AttachmentViewSet, TaskDocumentView

app_name = "tasks"

router = DefaultRouter()
router.register(r"groups", GroupViewSet)
router.register(r"lists", ListViewSet)
router.register(r"attachments", AttachmentViewSet)
router.register(r"^(?P<post_id>\d+)/comment", CommentViewSet)
'''router.register(r"^(?P<post_id>\d+)/attachment", AttachmentViewSet)'''
router.register(r"", PostViewSet)




from .views import Subscribe, Notify

urlpatterns = [
    path('subscribe/', Subscribe.as_view(), name='subscribe'),
    path('notify/', Notify.as_view(), name='notify'),
    #path('search/', SearchResultsList.as_view(), name='search-api'),
    path('search', TaskDocumentView.as_view()),
    path("", include(router.urls)),
    

]
