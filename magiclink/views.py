from django.conf import settings
from django.contrib.auth import login
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.generic.base import View

from .models import MagicToken

from hashids import Hashids

hashids = Hashids(salt=settings.SECRET_KEY)


class MagicTokenLogin(View):
    def get(self, request, token):
        token_id, user_id, ttl = hashids.decode(token)
        try:
            magictoken = MagicToken.objects.get(id=token_id)
        except MagicToken.DoesNotExist:
            return HttpResponseRedirect(reverse('login'))

        if not magictoken.valid:
            return HttpResponseRedirect(reverse('login'))

        user = magictoken.user
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        if request.user.is_authenticated():
            return HttpResponseRedirect(
                request.GET.get('next', reverse('home')))
        else:
            return HttpResponseRedirect(reverse('login'))
