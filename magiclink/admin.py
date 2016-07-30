from django.contrib import admin

from .models import MagicToken


@admin.register(MagicToken)
class MagicTokendmin(admin.ModelAdmin):
        list_display = ('user', 'ttl', 'magictoken')
        readonly_fields = ('__str__',)
