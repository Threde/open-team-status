from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from .models import Checkin


class CheckinDetailView(DetailView):
    model = Checkin

#@login_required
class CheckinCreateView(CreateView):
    model = Checkin
    fields = ['yesterday', 'goals_met', 'today', 'blockers']

    def form_valid(self, form):
        """set the user to the current user before saving."""
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

        return super(CheckinCreateView, self).form_valid(form)
