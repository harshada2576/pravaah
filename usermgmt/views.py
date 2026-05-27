from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


def _redirect_if_session_expired(request):
	if not request.user.is_authenticated:
		return redirect('usermgmt:session_expired')
	return None

# Create your views here.

def login_view(request):
	# Handle login form POST and render login template
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('usermgmt:admin_dashboard')
		else:
			messages.error(request, 'Invalid username or password')

	return render(request, 'auth/login.html')

def register_view(request):
	if request.method == 'POST':
		first_name = request.POST.get('first_name', '').strip()
		last_name = request.POST.get('last_name', '').strip()
		username = request.POST.get('username', '').strip()
		email = request.POST.get('email', '').strip()
		password = request.POST.get('password', '')
		confirm_password = request.POST.get('confirm_password', '')

		if not all([first_name, last_name, username, email, password, confirm_password]):
			messages.error(request, 'Please fill in all required fields.')
			return render(request, 'auth/register.html')

		if password != confirm_password:
			messages.error(request, 'Passwords do not match.')
			return render(request, 'auth/register.html')

		if User.objects.filter(username=username).exists():
			messages.error(request, 'Username already exists.')
			return render(request, 'auth/register.html')

		if User.objects.filter(email=email).exists():
			messages.error(request, 'Email already exists.')
			return render(request, 'auth/register.html')

		user = User.objects.create_user(
			username=username,
			email=email,
			password=password,
			first_name=first_name,
			last_name=last_name,
		)
		user.is_active = False
		user.save()

		uid = urlsafe_base64_encode(force_bytes(user.pk))
		token = default_token_generator.make_token(user)
		verify_link = request.build_absolute_uri(f'/verify-email/{uid}/{token}/')
		messages.success(request, f'Account created. Verification link: {verify_link}')
		return redirect('usermgmt:verify_email')

	return render(request, 'auth/register.html')

def forgot_password_view(request):
	if request.method == 'POST':
		email = request.POST.get('email')
		if email:
			messages.success(request, f'OTP sent to {email}.')
			return redirect('usermgmt:reset_password')
	return render(request, 'auth/forgot_password.html')

def reset_password_view(request):
	if request.method == 'POST':
		otp = request.POST.get('otp')
		new_password = request.POST.get('new_password')
		confirm_password = request.POST.get('confirm_password')
		if otp and new_password and new_password == confirm_password:
			messages.success(request, 'Password reset successfully.')
			return redirect('usermgmt:login')
		messages.error(request, 'Please provide a valid OTP and matching passwords.')
	return render(request, 'auth/reset_password.html')

def change_password_view(request):
	if request.method == 'POST':
		current_password = request.POST.get('current_password')
		new_password = request.POST.get('new_password')
		confirm_password = request.POST.get('confirm_password')
		if current_password and new_password and new_password == confirm_password:
			messages.success(request, 'Password changed successfully.')
			return redirect('usermgmt:login')
		messages.error(request, 'Please enter valid passwords.')
	return render(request, 'auth/change_password.html')

def session_expired_view(request):
	return render(request, 'auth/session_expired.html')

def verify_email_view(request, uidb64=None, token=None):
	if uidb64 and token:
		try:
			uid = force_str(urlsafe_base64_decode(uidb64))
			user = User.objects.get(pk=uid)
		except (TypeError, ValueError, OverflowError, User.DoesNotExist):
			messages.error(request, 'Invalid verification link.')
			return redirect('usermgmt:verify_email')

		if default_token_generator.check_token(user, token):
			user.is_active = True
			user.save(update_fields=['is_active'])
			messages.success(request, 'Email verified successfully. You can now login.')
			return redirect('usermgmt:login')

		messages.error(request, 'Verification link is invalid or expired.')
		return redirect('usermgmt:verify_email')

	if request.method == 'POST':
		messages.success(request, 'Verification email resent.')

	return render(request, 'auth/verify_email.html')

def admin_dashboard_view(request):
	redirect_response = _redirect_if_session_expired(request)
	if redirect_response:
		return redirect_response
	return render(request, 'rbac/admin_dashboard.html')

def roles_list_view(request):
	redirect_response = _redirect_if_session_expired(request)
	if redirect_response:
		return redirect_response
	return render(request, 'rbac/roles_list.html')

def role_form_view(request):
	redirect_response = _redirect_if_session_expired(request)
	if redirect_response:
		return redirect_response
	return render(request, 'rbac/role_form.html')

def permissions_list_view(request):
	redirect_response = _redirect_if_session_expired(request)
	if redirect_response:
		return redirect_response
	return render(request, 'rbac/permissions_list.html')

def assign_role_view(request):
	redirect_response = _redirect_if_session_expired(request)
	if redirect_response:
		return redirect_response
	return render(request, 'rbac/assign_role.html')

def assign_permissions_view(request):
	redirect_response = _redirect_if_session_expired(request)
	if redirect_response:
		return redirect_response
	return render(request, 'rbac/assign_permissions.html')

def permission_matrix_view(request):
	redirect_response = _redirect_if_session_expired(request)
	if redirect_response:
		return redirect_response
	return render(request, 'rbac/permission_matrix.html')
