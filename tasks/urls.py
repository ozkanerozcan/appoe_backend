from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import GroupViewSet, ListViewSet, CommentViewSet, PostViewSet, AttachmentViewSet

app_name = "tasks"

router = DefaultRouter()
router.register(r"groups", GroupViewSet)
router.register(r"lists", ListViewSet)
router.register(r"attachments", AttachmentViewSet)
router.register(r"^(?P<post_id>\d+)/comment", CommentViewSet)
'''router.register(r"^(?P<post_id>\d+)/attachment", AttachmentViewSet)'''
router.register(r"", PostViewSet)




urlpatterns = [
    path("", include(router.urls)),
]
