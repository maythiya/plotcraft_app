from django.contrib import admin
from .models import Timeline


@admin.register(Timeline)
class TimelineAdmin(admin.ModelAdmin):
	list_display = ('title', 'related_project', 'created_by', 'updated_at')
