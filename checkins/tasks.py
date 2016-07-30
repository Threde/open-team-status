from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

from magiclink.models import MagicToken

@shared_task
def send_reminder():
    for user in get_user_model().objects.all():
        if not user.email:
            continue
        link = MagicToken(user=user)
        link.save()
        send_mail(settings.OPEN_TEAM_STATUS_REMINDER_SUBJECT,
                  settings.OPEN_TEAM_STATUS_REMINDER_BODY.format(url=link),
                  settings.DEFAULT_FROM_EMAIL,
                  [user.email],
                  fail_silently=False)
