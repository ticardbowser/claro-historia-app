from django.urls import path
from . import views

urlpatterns = [
    # Home — list of dashboards
    path('', views.dashboards_home, name='dashboards_home'),

    # Dashboard views
    path('dashboard/<int:dashboard_id>/', views.dashboard, name='dashboard'),

    # Dashboard API
    path('api/dashboards/', views.dashboard_create, name='dashboard_create'),
    path('api/dashboards/<int:dashboard_id>/rename/', views.dashboard_rename, name='dashboard_rename'),
    path('api/dashboards/<int:dashboard_id>/delete/', views.dashboard_delete, name='dashboard_delete'),
    path('api/dashboards/<int:dashboard_id>/projects/', views.dashboard_add_project, name='dashboard_add_project'),
    path('api/dashboards/<int:dashboard_id>/projects/<int:project_id>/', views.dashboard_remove_project, name='dashboard_remove_project'),

    # Project pages
    path('project/<int:project_id>/', views.index, name='index'),

    # Project API
    path('api/projects/', views.project_create, name='project_create'),
    path('api/projects/<int:project_id>/rename/', views.project_rename, name='project_rename'),
    path('api/projects/<int:project_id>/delete/', views.project_delete, name='project_delete'),

    # Milestones API
    path('api/projects/<int:project_id>/milestones/', views.milestone_list, name='milestone_list'),
    path('api/projects/<int:project_id>/milestones/<int:milestone_id>/', views.milestone_detail, name='milestone_detail'),
    path('api/projects/<int:project_id>/milestones/<int:milestone_id>/cycle/', views.milestone_cycle, name='milestone_cycle'),

    # Events API
    path('api/projects/<int:project_id>/events/', views.event_list, name='event_list'),
    path('api/projects/<int:project_id>/events/<int:event_id>/', views.event_detail, name='event_detail'),
]
