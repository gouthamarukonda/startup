import json

from django.shortcuts import render

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.dateparse import parse_datetime
from datetime import datetime

from .models import Institute
from .models2 import InstituteAdmin
from userprofile.models import UserProfile, ROLE_INSTITUTE_ADMIN, STATUS_APPROVED
from userprofile.decorators import admin_required
from program.models import Program

@csrf_exempt
@admin_required
def institute_register(request):
	if request.method == 'POST':

		try:
			if not request.POST.get("institute_name"):
				return JsonResponse({"status": False, "msg": "Institute Name shouldn't be empty"})
			if not request.POST.get("address"):
				return JsonResponse({"status": False, "msg": "Address cannot be empty"})
			if not request.POST.get("city"):
				return JsonResponse({"status": False, "msg": "City can't be empty"})
			if not request.POST.get("state"):
				return JsonResponse({"status": False, "msg": "State can't be empty"})

			program_ids = json.loads(request.POST.get("program_list"))["program_list"]
			if not len(program_ids)==len(Program.objects.filter(pk__in = program_ids)):
				return JsonResponse({"status": False, "msg": "Some of the Program IDs are invalid or appear more than once"})

			institute = Institute()
			institute.institute_name = request.POST.get("institute_name")
			institute.address = request.POST.get("address")
			institute.city = request.POST.get("city")
			institute.state = request.POST.get("state")
			institute.phone_no = request.POST.get("phone_no")
			institute.manager_name = request.POST.get("manager_name")

			try:
				institute.save()
				institute.programs.add(*map(int, program_ids))
				return JsonResponse({"status": True, "msg": "Institute Registered Successfully"})
			except:
				return JsonResponse({"status": False, "msg": "Internal Server Error"})

		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})

@csrf_exempt
@admin_required
def register_admin(request):
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

			institute_ids = json.loads(request.POST.get("institute_list"))["institute_list"]
			if not len(institute_ids)==len(Institute.objects.filter(pk__in = institute_ids)):
				return JsonResponse({"status": False, "msg": "Some of the Institute IDs are invalid or appear more than once"})
				
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
			userprofile.role = ROLE_INSTITUTE_ADMIN
			userprofile.gender = request.POST.get("gender")
			userprofile.mobile = request.POST.get("mobile")
			userprofile.institute = institute
			userprofile.dob = datetime.now()
			userprofile.status = STATUS_APPROVED

			instituteAdmin = InstituteAdmin()
			instituteAdmin.user = userprofile

			try:
				userprofile.save()
				instituteAdmin.save()
				instituteAdmin.institutes.add(*map(int, institute_ids))
			except:
				user.delete()
				return JsonResponse({"status": False, "msg": "Internal Server Error"})

			return JsonResponse({"status": True, "msg": "Registered Successfully"})

		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})


@csrf_exempt
def get_all_institutes(request):
	if request.method == 'GET':
		try:
			resp = {"status": True}
			resp["institutes"] = []
			for institute in Institute.objects.all():
				odict={
					"institute_id" : institute.institute_id,
					"institute_name" : institute.institute_name,
					"institute_city" : institute.city,
					"institute_state" : institute.state,
				}
				resp["institutes"].append(odict)
			return JsonResponse(resp)
		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})
