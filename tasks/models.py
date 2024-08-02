import uuid
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

STATUS_CHOICES =(  
    (0, "To Do"),  
    (1, "Done"),  
    (2, "In Progress"),  

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

    list = models.ForeignKey(
        List,
        related_name="posts",
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ("-created_at",)

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
    file = models.FileField(upload_to = get_attachment_filename) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.body[:20]} by {self.created_by.username}"
