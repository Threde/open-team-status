# Disable djcelery admin
from django.contrib import admin
from djcelery.models import (TaskState, WorkerState,
                 PeriodicTask, IntervalSchedule, CrontabSchedule)

admin.site.unregister(TaskState)
admin.site.unregister(WorkerState)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(PeriodicTask)

# Re-title admin
admin.site.site_header = 'OpenTeamStatus administration'
