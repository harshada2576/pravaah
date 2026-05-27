from django.shortcuts import render

def admin_dashboard_view(request):
    return render(request, 'rbac/admin_dashboard.html')

def roles_list_view(request):
    return render(request, 'rbac/roles_list.html')

def role_form_view(request):
    return render(request, 'rbac/role_form.html')

def permissions_list_view(request):
    return render(request, 'rbac/permissions_list.html')

def assign_role_view(request):
    return render(request, 'rbac/assign_role.html')

def assign_permissions_view(request):
    return render(request, 'rbac/assign_permissions.html')

def permission_matrix_view(request):
    return render(request, 'rbac/permission_matrix.html')