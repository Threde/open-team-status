from django.contrib import admin


from .models import Checkin

@admin.register(Checkin)
class CheckinAdmin(admin.ModelAdmin):
        list_display = ('user', 'date', 'goals_met')
        list_filter = ('user', 'date', 'goals_met')
