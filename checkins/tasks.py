from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
import requests

from magiclink.models import MagicToken

from .models import Checkin


def make_magic_checkin_link(user):
    link = MagicToken(user=user)
    link.save()
    return '{}?next={}'.format(link, reverse('checkin-create'))

@shared_task
def slack_reminder():
    for user in get_user_model().objects.all():
        payload = {
            'channel': '@' + user.username,
            'text': settings.OPEN_TEAM_STATUS_REMINDER_BODY.format(
                url=make_magic_checkin_link(user)),
        }
        requests.post(settings.OPEN_TEAM_STATUS_SLACK_WEBHOOK,
                      json=payload)

@shared_task
def email_reminder():
    for user in get_user_model().objects.all():
        if not user.email:
            continue
        link = make_magic_checkin_link(user)
        send_mail(settings.OPEN_TEAM_STATUS_REMINDER_SUBJECT,
                  settings.OPEN_TEAM_STATUS_REMINDER_BODY.format(url=link),
                  settings.DEFAULT_FROM_EMAIL,
                  [user.email],
                  fail_silently=False)

def make_report_body():
    return settings.OPEN_TEAM_STATUS_REPORT_BODY.format(
        url='https://' + Site.objects.get_current().domain,
        checked_in=Checkin.objects.today().count(),
        goals_met=Checkin.objects.today().goals_met().count(),
        blocked=Checkin.objects.today().blocked().count(),
        total=get_user_model().objects.all().count(),
    )

@shared_task
def slack_report():
    requests.post(settings.OPEN_TEAM_STATUS_SLACK_WEBHOOK, json={
        'channel': settings.OPEN_TEAM_STATUS_REPORT_SLACK_CHANNEL,
        'text': make_report_body(),
    })

@shared_task
def email_report():
    for user in get_user_model().objects.all():
        if not user.email:
            continue
        send_mail(settings.OPEN_TEAM_STATUS_REPORT_SUBJECT,
                  make_report_body(),
                  settings.DEFAULT_FROM_EMAIL,
                  [user.email],
                  fail_silently=False)
