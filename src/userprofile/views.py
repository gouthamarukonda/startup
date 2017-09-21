from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import get_default_password_validators
from django.core.exceptions import ValidationError
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from institute.models import Institute
from program.models import Standard, Program
from institute.models2 import InstituteAdmin
from student.models import StudentProfile, BoardOfEducation
from teacher.models import TeacherProfile
from userprofile.decorators import admin_required
from userprofile.models import STATUS_APPROVED, STATUS_UNAPPROVED, ROLE_TEACHER, ROLE_STUDENT, UserProfile, ROLE_INSTITUTE_ADMIN


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
						if user.userprofile.role == ROLE_INSTITUTE_ADMIN:
							return JsonResponse({"status": True , "msg": "institute admin login"})
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
		institutes = []
		for institute in Institute.objects.all():
			odict = {
				"institute_id": institute.institute_id,
				"institute_name": institute.institute_name,
				"institute_city": institute.city,
				"institute_state": institute.state,
			}
			institutes.append(odict)
		programs = []
		for program in Program.objects.all():
			odict = {
				"program_id": program.program_id,
				"program_name": program.program_name,
			}
			programs.append(odict)
		standards = []
		for standard in Standard.objects.all():
			odict = {
				"standard_id": standard.standard_id,
				"standard_name": standard.standard_name,
			}
			standards.append(odict)
		boes = []
		for boe in BoardOfEducation.objects.all():
			odict = {
				"boe_id": boe.boe_id,
				"boe_name": boe.boe_name,
			}
			boes.append(odict)
		return render(request, 'register.html', {'institutes' : institutes, 'programs' : programs, 'standards' : standards, 'boes' : boes})

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
		elif request.user.userprofile.role == ROLE_TEACHER:
			return render(request, 'teacher/index.html')
		elif request.user.userprofile.role == ROLE_INSTITUTE_ADMIN:
			return render(request, 'instituteadmin/index.html')
		elif request.user.userprofile.role == ROLE_STUDENT:
			return render(request, 'student/index.html', {'image' : request.user.userprofile.get_profile_picture_url()})
		else:
			return HttpResponse(status=500)

@admin_required
def get_admin_home_page(request):
	NumInstitutes = len(Institute.objects.all())
	NumStudents = len(StudentProfile.objects.all())
	NumTeachers = len(TeacherProfile.objects.all())
	NumInstituteAdmins = len(InstituteAdmin.objects.all())
	return render(request, 'adminportal/index.html',
				  {'NumInstitutes': NumInstitutes, 'NumStudents': NumStudents, 'NumTeachers': NumTeachers,
				   'NumInstituteAdmins': NumInstituteAdmins})

@csrf_exempt
@login_required(login_url='/login/')
def update_profile_picture(request):
	if request.method == 'POST':

		try:
			if not request.FILES:
				return JsonResponse({"status": False, "msg": "profile_picture shouldn't be empty"})

			user_profile = request.user.userprofile
			if user_profile.profile_picture:
				user_profile.profile_picture.delete()

			user_profile.profile_picture = request.FILES['profile_picture']
			user_profile.profile_picture.name = request.user.username
			user_profile.save()
			return JsonResponse({"status": True, "msg": "Profile Picture Updated Successfully"})
		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})

@csrf_exempt
@login_required(login_url='/login/')
def get_profile_picture(request):

	if request.method == 'GET':
		try:
			profile_pic_url = request.user.userprofile.get_profile_picture_url()
			return HttpResponse("<img src='" + profile_pic_url + "'>")
		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})

	elif request.method == 'POST':

		try:
			if not request.POST.get("username"):
				return JsonResponse({"status": False, "msg": "Username shouldn't be empty"})
			if not User.objects.filter(username = request.POST.get("username")).exists():
				return JsonResponse({"status": True, "msg": "Username does not exists"})

			profile_pic_url = UserProfile.objects.get(user__username = request.POST.get("username")).get_profile_picture_url()
			return HttpResponse("<img src='" + profile_pic_url + "'>")
		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})
