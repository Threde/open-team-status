from celery import shared_task
from django.contrib.sites.models import Site
import requests

@shared_task
def heroku_keepalive():
    requests.get('https://' + Site.objects.get_current().domain)
