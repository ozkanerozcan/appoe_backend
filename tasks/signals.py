
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail
from urllib.parse import urlparse

from .models import Attachment, Post
import os
import shutil


@receiver(post_delete, sender=Attachment)
def delete_file(sender, instance, **kwargs):
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)
    
@receiver(post_delete, sender=Post)
def delete_folder(sender, instance, **kwargs):
    # Combine the media root with the parsed path
    folderPath = settings.MEDIA_ROOT + "/task/" + str(instance.id)

    if os.path.isdir(folderPath):
        shutil.rmtree(folderPath)
