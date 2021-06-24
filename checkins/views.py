from celery.execute import send_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from .models import Checkin

if settings.OPEN_TEAM_STATUS_PUBLIC:
    configurable_login_required = []
else:
    configurable_login_required = [login_required]

@method_decorator(configurable_login_required, name='dispatch')
class CheckinDayView(ListView):
    model = Checkin

    def _get_day(self):
        if self.kwargs['day'] == 'today':
            return timezone.now().date()
        else:
            return timezone.datetime.strptime(self.kwargs['day'],
                                             '%Y-%m-%d').date()

    def get_queryset(self, **kwargs):
        return Checkin.objects.filter(date=self._get_day())

    def get_context_data(self, **kwargs):
        context = super(CheckinDayView, self).get_context_data(**kwargs)
        context['date'] = self._get_day()
        context['next'] = (self._get_day() +
                           timezone.timedelta(days=1)).strftime('%Y-%m-%d')
        context['today'] = timezone.now().date()
        context['prev'] = (self._get_day() +
                           timezone.timedelta(days=-1)).strftime('%Y-%m-%d')

        users = get_user_model().objects.filter(
            date_joined__lte=self._get_day() + timezone.timedelta(days=1))
        context['num_users'] = users.count()
        users_missing_checkins = users.exclude(
            id__in=context['object_list'].values_list('user_id', flat=True))
        context['missing_checkins'] = [{'user': u}
                                       for u in users_missing_checkins]

        return context


@method_decorator(login_required, name='dispatch')
class CheckinDetailView(DetailView):
    model = Checkin

@method_decorator(login_required, name='dispatch')
class CheckinCreateView(CreateView):
    model = Checkin
    fields = ['yesterday', 'goals_met', 'today', 'blockers']

    def get_context_data(self, **kwargs):
        context = super(CheckinCreateView, self).get_context_data(**kwargs)
        try:
            context['yesterday'] = Checkin.objects.yesterday().get(
                user=self.request.user).today
        except Checkin.DoesNotExist:
            pass
        return context

    def get_initial(self):
        try:
            checkin = Checkin.objects.get(date=timezone.now().date(),
                                          user=self.request.user)
            return {f: getattr(checkin, f) for f in self.fields}
        except Checkin.DoesNotExist:
            return {}

    def form_valid(self, form):
        """set the user to the current user before saving and update if same day"""
        self.object, created = Checkin.objects.update_or_create(
            user=self.request.user, date=timezone.now().date(),
            defaults=form.cleaned_data)

        if created:
            send_task(settings.OPEN_TEAM_STATUS_CHECKIN_TASK,
                      (self.object.id,))

        return HttpResponseRedirect(reverse(
            'checkin-day', kwargs={'day': 'today'}))
