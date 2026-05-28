from django.shortcuts import render
from .models import User
from .models import Role
from .models import AuditLog
from django.core.paginator import Paginator
from .models import User
from .models import Role
from django.contrib.auth.decorators import login_required
from .forms import ProfileEditForm
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator
def home(request):
    return render(
        request,
        'accounts/profile.html'
    )
@login_required
def profile(request):
    context = {
        'user_data': request.user
    }
    return render(
        request,
        'accounts/profile.html',
        context
    )
@login_required
def profile_edit(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileEditForm(
            request.POST,
            instance=user
        )
        if form.is_valid():
            form.save()
            # AUDIT LOG
            AuditLog.objects.create(
                user=user,
                action='Profile Updated',
                ip_address=request.META.get(
                    'REMOTE_ADDR'
                )
            )
            messages.success(
                request,
                'Profile updated successfully.'

            )

            return redirect(
                '/profile/'
            )
    else:
        form = ProfileEditForm(
            instance=user
        )

    context = {

        'form': form

    }

    return render(

        request,

        'accounts/profile_edit.html',

        context

    )


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(
            request.user,
            request.POST
        )
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(
                request,
                user
            )
            messages.success(
                request,
                'Password changed successfully.'
            )
            return redirect(
                '/profile/'
            )

    else:

        form = PasswordChangeForm(
            request.user
        )

    context = {

        'form': form

    }

    return render(

        request,

        'accounts/change_password.html',

        context

    )

def audit_logs(request):

    logs = AuditLog.objects.all().order_by(
        '-created_at'
    )

    # SEARCH

    search = request.GET.get(
        'search'
    )

    if search:

        logs = logs.filter(
            user__username__icontains=search
        )

    # ACTION FILTER

    action = request.GET.get(
        'action'
    )

    if action:

        logs = logs.filter(
            action=action
        )

    # PAGINATION

    paginator = Paginator(
        logs,
        10
    )

    page_number = request.GET.get(
        'page'
    )

    page_obj = paginator.get_page(
        page_number
    )

    context = {

        'logs': page_obj,

        'page_obj': page_obj,

        'search': search,

        'selected_action': action

    }

    return render(

        request,

        'accounts/audit_logs.html',

        context

    )
@login_required
def activity_dashboard(request):

    total_users = User.objects.count()

    total_logs = AuditLog.objects.count()

    total_roles = Role.objects.count()

    login_count = AuditLog.objects.filter(
        action='Login'
    ).count()

    recent_logs = AuditLog.objects.all().order_by(
        '-created_at'
    )[:5]

    # -------------------------
    # ROLE DISTRIBUTION
    # -------------------------

    admin_count = User.objects.filter(
        role__role_name='Admin'
    ).count()

    manager_count = User.objects.filter(
        role__role_name='Manager'
    ).count()

    qa_count = User.objects.filter(
        role__role_name='QA'
    ).count()

    # -------------------------
    # STATUS COUNTS
    # -------------------------

    active_users = User.objects.filter(
        status='Active'
    ).count()

    inactive_users = User.objects.filter(
        status='Inactive'
    ).count()

    # -------------------------
    # AUDIT ACTIONS
    # -------------------------

    login_actions = AuditLog.objects.filter(
        action='Login'
    ).count()

    logout_actions = AuditLog.objects.filter(
        action='Logout'
    ).count()

    update_actions = AuditLog.objects.filter(
        action='Profile Updated'
    ).count()

    context = {

        'total_users': total_users,

        'total_logs': total_logs,

        'total_roles': total_roles,

        'login_count': login_count,

        'recent_logs': recent_logs,

        # ROLE DATA

        'admin_count': admin_count,

        'manager_count': manager_count,

        'qa_count': qa_count,

        # STATUS DATA

        'active_users': active_users,

        'inactive_users': inactive_users,

        # AUDIT DATA

        'login_actions': login_actions,

        'logout_actions': logout_actions,

        'update_actions': update_actions

    }

    return render(

        request,

        'accounts/activity_dashboard.html',

        context

    )

def reports(request):

    return render(
        request,
        'accounts/reports.html'
    )


def report_result(request):

    report_type = request.GET.get(
        'report_type'
    )

    role = request.GET.get(
        'role'
    )

    data = []

    # -------------------------
    # USERS REPORT
    # -------------------------

    if report_type == 'users':

        users = User.objects.all()

        if role:

            users = users.filter(
                role__role_name=role
            )

        data = users

    # -------------------------
    # ROLE REPORT
    # -------------------------

    elif report_type == 'roles':

        users = User.objects.all()

        if role:

            users = users.filter(
                role__role_name=role
            )

        data = users

    # -------------------------
    # LOGIN REPORT
    # -------------------------

    elif report_type == 'logins':

        logs = AuditLog.objects.filter(
            action='Login'
        )

        data = logs

    context = {

        'report_type': report_type,

        'data': data

    }

    return render(

        request,

        'accounts/report_result.html',

        context

    )

@login_required
def users_list(request):

    users = User.objects.all().order_by(
        '-created_at'
    )

    # SEARCH

    search = request.GET.get(
        'search'
    )

    if search:

        users = users.filter(
            username__icontains=search
        )

    # PAGINATION

    paginator = Paginator(
        users,
        10
    )

    page_number = request.GET.get(
        'page'
    )

    page_obj = paginator.get_page(
        page_number
    )

    context = {

        'users': page_obj,

        'page_obj': page_obj,

        'search': search

    }

    return render(

        request,

        'accounts/users_list.html',

        context

    )