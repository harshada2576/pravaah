from django.urls import path
from . import views  # This safely grabs views from the local directory

app_name = 'usermgmt'

urlpatterns = [
    path('rbac/dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
    path('rbac/roles/', views.roles_list_view, name='roles_list'),
    path('rbac/roles/add/', views.role_form_view, name='role_add'),
    path('rbac/permissions/', views.permissions_list_view, name='permissions_list'),
    path('rbac/assign-role/', views.assign_role_view, name='assign_role'),
    path('rbac/assign-permissions/', views.assign_permissions_view, name='assign_permissions'),
    path('rbac/matrix/', views.permission_matrix_view, name='permission_matrix'),
]