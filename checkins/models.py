from django.core.urlresolvers import reverse
from django.conf import settings
from django.db import models


class Checkin(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    yesterday = models.TextField(blank=True)
    goals_met = models.BooleanField(default=False)
    today = models.TextField(blank=True)
    blockers = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse('checkin-detail', args=[str(self.id)])
