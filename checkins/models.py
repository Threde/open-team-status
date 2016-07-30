from django.core.urlresolvers import reverse
from django.conf import settings
from django.db import models
from django.utils import timezone


class CheckinQuerySet(models.QuerySet):
    def blocked(self):
        return self.exclude(blockers='')

    def goals_met(self):
        return self.filter(goals_met=True)

    def today(self):
        return self.filter(date=timezone.now().date())

    def yesterday(self):
        return self.filter(date=timezone.now().date() -
                           timezone.timedelta(days=1))

class Checkin(models.Model):
    objects = CheckinQuerySet.as_manager()

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    yesterday = models.TextField(blank=True)
    goals_met = models.BooleanField(default=False)
    today = models.TextField(blank=True)
    blockers = models.TextField(blank=True)

    class Meta:
        unique_together = ('user', 'date')

    def get_absolute_url(self):
        return reverse('checkin-detail', args=[str(self.id)])
