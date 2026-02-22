from django.contrib import admin
from .models import JobcardTemplate, Jobcard, LineItem

admin.site.register(JobcardTemplate)
admin.site.register(LineItem)

@admin.register(Jobcard)
class JobcardAdmin(admin.ModelAdmin):
    list_display = ('jobcard_id', 'client', 'technician', 'status')
