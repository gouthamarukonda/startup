from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import get_default_password_validators
from django.core.exceptions import ValidationError
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from userprofile.decorators import admin_required
from userprofile.models import STATUS_APPROVED, STATUS_UNAPPROVED, ROLE_TEACHER, ROLE_STUDENT


@csrf_exempt
@admin_required
def user_disapprove(request):
	if request.method == 'POST':
		try:
			if not request.POST.get("username"):
				return JsonResponse({"status": False, "msg": "User ID shouldn't be empty"})
			else:
				if User.objects.filter(username = request.POST.get("username")).exists():
					user = User.objects.get(username = request.POST.get("username"))
					user.userprofile.status = STATUS_UNAPPROVED
					user.userprofile.save()
					user.save()
					return JsonResponse({"status": True, "msg": "User DisApproved Sucessfully"})
				else:
					return JsonResponse({"status": False, "msg": "User Doesn't exist"})

		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})

@csrf_exempt
def user_login(request):
	if request.method == 'POST':
		try:
			if not request.POST.get("username"):
				return JsonResponse({"status": False, "msg": "User ID shouldn't be empty"})
			else:
				if User.objects.filter(username = request.POST.get("username")).exists():
					user_object = User.objects.get(username = request.POST.get("username"))
					if not(user_object.is_superuser):
						if user_object.userprofile.status != STATUS_APPROVED :
							return JsonResponse({"status": False, "msg": "Wait for your approval"})
					user = authenticate(username = request.POST.get("username"), password = request.POST.get("password"))
					if user is not None:
						login(request, user)
						if user.is_superuser:
							return JsonResponse({"status": True , "msg": "admin login"})
						if user.userprofile.role == ROLE_STUDENT:
							return JsonResponse({"status": True , "msg": "student login"})
						if user.userprofile.role == ROLE_TEACHER:
							return JsonResponse({"status": True , "msg": "teacher login"})
					else:
						return JsonResponse({"status": False, "msg": "Credentials don't match"})
				else:
					return JsonResponse({"status": False, "msg": "User Doesn't exist"})
		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})

def get_login_page(request):
	if request.method == 'GET':
		if request.user.is_authenticated():
			return HttpResponseRedirect('/user/home/')
		return render(request, 'login.html')

def register(request):
	if request.method == 'GET':
		if request.user.is_authenticated():
			logout(request)
		return render(request, 'register.html')

@login_required(login_url='/login/')
@csrf_exempt
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/login/')

@csrf_exempt
def username_verification(request):
	if request.method == 'POST':
		try:
			if not request.POST.get("username"):
				return JsonResponse({"status": False, "msg": "User ID shouldn't be empty"})
			if not User.objects.filter(username = request.POST.get("username")).exists():
				return JsonResponse({"status": True, "msg": "User ID does not exists"})
			else:
				return JsonResponse({"status": False, "msg": "User ID already exists"})
		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})

@csrf_exempt
def email_verification(request):
	if request.method == 'POST':
		try:
			if not request.POST.get("email"):
				return JsonResponse({"status": False, "msg": "Email ID shouldn't be empty"})
			if not User.objects.filter(email = request.POST.get("email")).exists():
				return JsonResponse({"status": True, "msg": "Email ID does not exists"})
			else:
				return JsonResponse({"status": False, "msg": "Email ID already exists"})	
		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})

@csrf_exempt
def password_validation(request):
	if request.method == 'POST':
		try:
			if not request.POST.get("username"):
				return JsonResponse({"status": False, "msg": "Username shouldn't be empty"})

			if not request.POST.get("password"):
				return JsonResponse({"status": False, "msg": "Password shouldn't be empty"})

			user = None
			if request.POST.get("username"):
				user = User(username = request.POST.get("username"))
				user.first_name = request.POST.get("first_name")
				user.last_name = request.POST.get("last_name")
				user.email = request.POST.get("email")

			password = request.POST.get("password")
			password_validators = get_default_password_validators()
			passed, failed = [], []

			for validator in password_validators:
				try:
					validator.validate(password, user)
					passed.append(validator.get_help_text())
				except ValidationError:
					failed.append(validator.get_help_text())

			if len(failed) == 0:
				return JsonResponse({"status": True, "passed": passed})
			else:
				return JsonResponse({"status": False, "passed": passed, "failed": failed})
		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})


@login_required(login_url='/login/')
def get_user_home_page(request):
	if request.method == 'GET':
		if request.user.is_superuser:
			return get_admin_home_page(request)
		elif request.user.userprofile.role == 1:
			return render(request, 'teacher/index.html')
		elif request.user.userprofile.role == 2:
			return render(request, 'instituteadmin/index.html')
		else:
			return render(request, 'student/index.html')


@login_required(login_url='/login/')
def get_admin_home_page(request):
	return render(request, 'adminportal/index.html')
