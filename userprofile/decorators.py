from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from userprofile.models import ROLE_STUDENT, ROLE_TEACHER, ROLE_INSTITUTE_ADMIN, STATUS_APPROVED

def admin_required(func):
	@login_required(login_url='/login/')
	def authorize(request, *args, **kwargs):
		if request.user.is_superuser:
			return func(request, *args, **kwargs)
		return JsonResponse({"status": "Not-Authorized"})
	return authorize

def institute_admin_required(func):
	@login_required(login_url='/login/')
	def authorize(request, *args, **kwargs):
		if request.user.userprofile.role == ROLE_INSTITUTE_ADMIN:
			return func(request, *args, **kwargs)
		return JsonResponse({"status": "Not-Authorized"})
	return authorize

def admin_teacher_required(func):
	@login_required(login_url='/login/')
	def authorize(request, *args, **kwargs):
		if request.user.is_superuser or request.user.userprofile.role == ROLE_TEACHER:
			return func(request, *args, **kwargs)
		return JsonResponse({"status": "Not-Authorized"})
	return authorize

def teacher_required(func):
	@login_required(login_url='/login/')
	def authorize(request, *args, **kwargs):
		if request.user.userprofile.role == ROLE_TEACHER:
			return func(request, *args, **kwargs)
		return JsonResponse({"status": "Not-Authorized"})
	return authorize

def student_required(func):
	@login_required(login_url='/login/')
	def authorize(request, *args, **kwargs):
		if request.user.userprofile.role == ROLE_STUDENT:
			return func(request, *args, **kwargs)
		return JsonResponse({"status": "Not-Authorized"})
	return authorize

def approved_student_required(func):
	@login_required(login_url='/login/')
	def authorize(request, *args, **kwargs):
		if request.user.userprofile.status == STATUS_APPROVED and request.user.userprofile.role == ROLE_STUDENT:
			return func(request, *args, **kwargs)
		return JsonResponse({"status": "Not-Authorized"})
	return authorize

def approved_teacher_required(func):
	@login_required(login_url='/login/')
	def authorize(request, *args, **kwargs):
		if request.user.userprofile.status == STATUS_APPROVED and request.user.userprofile.role == ROLE_TEACHER:
			return func(request, *args, **kwargs)
		return JsonResponse({"status": "Not-Authorized"})
	return authorize

def approved_user_required(func):
	@login_required(login_url='/login/')
	def authorize(request, *args, **kwargs):
		if request.user.userprofile.status == STATUS_APPROVED:
			return func(request, *args, **kwargs)
		return JsonResponse({"status": "Not-Authorized"})
	return authorize
