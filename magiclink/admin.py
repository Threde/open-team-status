from django.contrib import admin

from .models import MagicToken


@admin.register(MagicToken)
class MagicTokendmin(admin.ModelAdmin):
        list_display = ('user', 'created', 'ttl', '__str__')
        list_filter = ('created', 'user')
        readonly_fields = ('created', '__str__')
