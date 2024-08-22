from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail

import os
import shutil

User = get_user_model()

@receiver(post_save, sender=User)
def send_activation_mail(sender, instance, created, **kwargs):
    if created:
        url = f'{settings.WEBSITE_URL}/activate/?email={instance.email}&id={instance.id}'

        print(url)

        send_mail(
            "Please verify your email",
            f"The url for activating your account is: {url}",
            "noreply@ozkanerozcan.com",
            [instance.email],
            fail_silently=False,
        )

@receiver(pre_save, sender=User)
def delete_folder(sender, instance, **kwargs):
    print('pk',instance.pk)
    if instance.pk:  # Check if this is an update (not a new user)
        old_avatar = User.objects.get(pk=instance.pk).avatar  # Get the old avatar
        new_avatar = instance.avatar  # Get the new avatar being set
        print('old_avatar',old_avatar)
        print('new_avatar',new_avatar)
        
        # Compare old and new avatar only if new_avatar is not None (not cleared)
        if old_avatar and new_avatar and old_avatar != new_avatar:
            # Combine the media root with the parsed path
            folderPath = settings.MEDIA_ROOT + "/user/" + str(instance.username) + "/avatar" 
            print('folderpath', folderPath)
            if os.path.isdir(folderPath):
                shutil.rmtree(folderPath)


            

@receiver(post_delete, sender=User)
def delete_folder(sender, instance, **kwargs):

    # Combine the media root with the parsed path
    folderPath = settings.MEDIA_ROOT + "/user/" + str(instance.username) + "/avatar" 

    if os.path.isdir(folderPath):
        shutil.rmtree(folderPath)
