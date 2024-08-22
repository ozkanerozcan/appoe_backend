import uuid
from datetime import datetime
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from django_resized import ResizedImageField
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField 



STATUS_CHOICES =(  
    (0, "To Do"),  
    (1, "Done"),  
    (2, "In Progress"),  

) 

WORKED_ON_CHOICES =(  
    (0, "Office"),  
    (1, "Manufacturer"),  
    (2, "Customer"),  
    (3, "Home"),

) 

class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(_("Group title"), max_length=100)
    body = models.TextField(_("Group body"),blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='task_post_groups', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Group")
        verbose_name_plural = _("Groups")
        ordering = ('-created_at',)
    
    def created_at_timesince(self):
       return timesince(self.created_at)

    def __str__(self):
        return self.title

class List(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(_("List title"), max_length=100)
    body = models.TextField(_("List body"),blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='task_post_lists', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    group = models.ForeignKey(Group, related_name="lists", blank=True,  null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("List")
        verbose_name_plural = _("Lists")
        ordering = ('-created_at',)
    
    def created_at_timesince(self):
       return timesince(self.created_at)

    def __str__(self):
        return self.title


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(_("Post title"), max_length=250)
    body = models.TextField(_("Post body"), blank=True, null=True)
    status = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="task_posts",
        null=True,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deadline_at = models.DateTimeField(default=datetime.now)
    worked_on = models.IntegerField(choices = WORKED_ON_CHOICES, default=0) 


    list = models.ForeignKey(
        List,
        related_name="posts",
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ("-deadline_at",)


    def __str__(self):
        return f"{self.title} by {self.created_by.username}"
    



class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    body = models.TextField(_("Comment body"), blank=True, null=True)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="task_post_comments",
        null=True,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.body[:20]} by {self.created_by.username}"

def get_attachment_filename(instance, filename):
    return f"task/{instance.post.id}/attachment/{filename}"

class Attachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    body = models.TextField(_("Attachment body"), blank=True, null=True)
    post = models.ForeignKey(Post, related_name="attachments", on_delete=models.CASCADE)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="task_post_attachments",
        null=True,
        on_delete=models.CASCADE,
    )
    #file = models.FileField(upload_to = get_attachment_filename) 
    file = ResizedImageField(force_format="WEBP", quality=80, upload_to = get_attachment_filename )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.body[:20]} by {self.created_by.username}"



class Subscription(models.Model):
    endpoint = models.TextField()
    p256dh = models.TextField()
    auth = models.TextField()

    def __str__(self):
        return self.endpoint