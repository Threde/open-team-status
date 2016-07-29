import datetime

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from .models import Checkin


class CheckinTodayView(ListView):
    model = Checkin

    def get_query_set(self, request):
        return Checkin.objects.filter(date=datetime.date.today())


class CheckinDetailView(DetailView):
    model = Checkin

#@login_required
class CheckinCreateView(CreateView):
    model = Checkin
    fields = ['yesterday', 'goals_met', 'today', 'blockers']

    def form_valid(self, form):
        """set the user to the current user before saving and update if same day"""
        self.object, created = Checkin.objects.update_or_create(
            user=self.request.user, date=datetime.date.today(),
            defaults=form.cleaned_data)

        return HttpResponseRedirect(reverse('checkin-today'))