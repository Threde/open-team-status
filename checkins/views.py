import datetime

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from .models import Checkin


class CheckinDayView(ListView):
    model = Checkin

    def get_queryset(self, **kwargs):
        if self.kwargs['day'] == 'today':
            day = datetime.date.today()
        else:
            day = datetime.datetime.strptime(self.kwargs['day'],
                                             '%Y-%m-%d').date()
        return Checkin.objects.filter(date=day)


class CheckinDetailView(DetailView):
    model = Checkin

#@login_required
class CheckinCreateView(CreateView):
    model = Checkin
    fields = ['yesterday', 'goals_met', 'today', 'blockers']

    def get_initial(self):
        try:
            checkin = Checkin.objects.get(date=datetime.date.today(),
                                          user=self.request.user)
            return {f: getattr(checkin, f) for f in self.fields}
        except Checkin.DoesNotExist:
            return {}

    def form_valid(self, form):
        """set the user to the current user before saving and update if same day"""
        self.object, created = Checkin.objects.update_or_create(
            user=self.request.user, date=datetime.date.today(),
            defaults=form.cleaned_data)

        return HttpResponseRedirect(reverse(
            'checkin-day', kwargs={'day': 'today'}))
