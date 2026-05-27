from django.urls import path
from . import views
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
urlpatterns = [
    path('', views.home, name='home'),
    path(
        'profile/',
        views.profile,
        name='profile'
    ),
    path(
        'profile/edit/',
        views.profile_edit,
        name='profile_edit'
    ),
    path(
        'change-password/',
        views.change_password,
        name='change_password'
    ),

    path(
        'audit-logs/',
        views.audit_logs,
        name='audit_logs'
    ),

    path(
        'activity-dashboard/',
        views.activity_dashboard,
        name='activity_dashboard'
    ),

    path(
        'reports/',
        views.reports,
        name='reports'
    ),

    path(
        'report-result/',
        views.report_result,
        name='report_result'
    ),

    path(
        'users-list/',
        views.users_list,
        name='users_list'
    ),
]