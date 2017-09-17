from django.shortcuts import render

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.dateparse import parse_datetime
from datetime import datetime

from student.models import StudentProfile, STD_CHOICES
from userprofile.models import UserProfile, ROLE_STUDENT, STATUS_UNAPPROVED
from institute.models import Institute

@csrf_exempt
def student_register(request):

	if request.method == 'POST':

		try:
			if not request.POST.get("username"):
				return JsonResponse({"status": False, "msg": "Username shouldn't be empty"})
			if User.objects.filter(username = request.POST.get("username")).exists():
				return JsonResponse({"status": False, "msg": "Given Username already in use"})
			if User.objects.filter(email = request.POST.get("email")).exists():
				return JsonResponse({"status": False, "msg": "Given email already in use"})

			if not request.POST.get("password"):
				return JsonResponse({"status": False, "msg": "Password cannot be empty"})
			if not request.POST.get("password_again"):
				return JsonResponse({"status": False, "msg": "Retype password can't be empty"})
			if request.POST.get("password") != request.POST.get("password_again"): 
				return JsonResponse({"status": False, "msg": "Password and retype password must be the same"})

			if request.POST.get("standard") not in [choice[0] for choice in STD_CHOICES]: 
				return JsonResponse({"status": False, "msg": "Invalid Standard Value"})

			institute = None
			try:
				institute = Institute.objects.get(institute_id = request.POST.get("institute"))
			except:
				return JsonResponse({"status": False, "msg": "Given Institute Doesnt Exist"})

			user = User()
			user.username = request.POST.get("username")
			user.first_name = request.POST.get("firstname")
			user.last_name = request.POST.get("lastname")
			user.email = request.POST.get("email")
			user.set_password(request.POST.get("password"))

			try:
				user.save()
			except:
				return JsonResponse({"status": False, "msg": "Internal Server Error"})

			userprofile = UserProfile()
			userprofile.user = user
			userprofile.role = ROLE_STUDENT
			userprofile.gender = request.POST.get("gender")
			userprofile.mobile = request.POST.get("mobile")
			userprofile.institute = institute
			userprofile.dob = datetime.now()
			userprofile.status = STATUS_UNAPPROVED

			studentprofile = StudentProfile()
			studentprofile.user = userprofile
			studentprofile.boe = request.POST.get("boe")
			studentprofile.standard = request.POST.get("standard")
			studentprofile.roll_number = request.POST.get("roll_number")

			try:
				userprofile.save()
				userprofile.programs.add(request.POST.get("program_id"))
				studentprofile.save()
			except:
				user.delete()
				return JsonResponse({"status": False, "msg": "Internal Server Error"})

			return JsonResponse({"status": True, "msg": "Registered Successfully"})

		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})
