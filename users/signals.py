from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail

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
