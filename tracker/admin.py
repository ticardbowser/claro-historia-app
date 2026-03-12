from django.contrib import admin
from .models import Project, Milestone, Event


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'date', 'cat', 'project']
    list_filter = ['status', 'project']
    search_fields = ['title', 'desc']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'etype', 'date', 'people', 'project']
    list_filter = ['etype', 'project']
    search_fields = ['title', 'desc']
