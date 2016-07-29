"""openteamstatus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

import checkins.views


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', RedirectView.as_view(url=reverse_lazy(
        'checkin-day', kwargs={'day': 'today'}))),

    url(r'^checkin/$',
        checkins.views.CheckinCreateView.as_view(),
        name='checkin-create'),
    url(r'^checkin/(?P<pk>\d+)/$',
        checkins.views.CheckinDetailView.as_view(),
        name='checkin-detail'),

    url(r'^checkins/(?P<day>\d{4}-\d{2}-\d{2}|today)/$',
        checkins.views.CheckinDayView.as_view(),
        name='checkin-day'),

    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
]
