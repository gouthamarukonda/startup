from django.shortcuts import render

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.password_validation import get_default_password_validators
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils.dateparse import parse_datetime

from datetime import datetime

from teacher.models import TeacherProfile
from userprofile.models import UserProfile, ROLE_TEACHER, STATUS_UNAPPROVED, GENDER_CHOICES
from institute.models import Institute
from approval.models import ApprovalRequest
from approval.approvalTypes import APPROVAL_TEACHER_REGISTRATION

@csrf_exempt
def teacher_register(request):

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
			if not request.POST.get("repeat_password"):
				return JsonResponse({"status": False, "msg": "Retype password can't be empty"})
			if request.POST.get("password") != request.POST.get("repeat_password"): 
				return JsonResponse({"status": False, "msg": "Password and retype password must be the same"})
			if request.POST.get("gender") not in [choice[0] for choice in GENDER_CHOICES]: 
				return JsonResponse({"status": False, "msg": "Invalid Gender Value"})
			if not request.POST.get("program_id"):
				return JsonResponse({"status": False, "msg": "Program ID shouldn't be empty"})

			user = None
			if request.POST.get("username"):
				user = User(username=request.POST.get("username"))
				user.first_name = request.POST.get("firstname")
				user.last_name = request.POST.get("lastname")
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
			if len(failed) != 0:
				return JsonResponse({"status": False, "msg": failed})

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
			userprofile.role = ROLE_TEACHER
			userprofile.gender = request.POST.get("gender")
			userprofile.mobile = request.POST.get("mobile")
			userprofile.institute = institute
			userprofile.address = request.POST.get("address")
			userprofile.dob = datetime.now()
			userprofile.status = STATUS_UNAPPROVED

			teacherprofile = TeacherProfile()
			teacherprofile.user = userprofile
			teacherprofile.experience = request.POST.get("experience")

			try:
				userprofile.save()
				userprofile.programs.add(request.POST.get("program_id"))
				teacherprofile.save()
			except:
				user.delete()
				return JsonResponse({"status": False, "msg": "Internal Server Error"})

			registration_approval_request = ApprovalRequest(approval_type = APPROVAL_TEACHER_REGISTRATION, user = user)
			registration_approval_request.save()

			return JsonResponse({"status": True, "msg": "Registered Successfully"})

		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})
