from datetime import datetime

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from approval.approvalTypes import APPROVAL_STUDENT_REGISTRATION
from django.contrib.auth.password_validation import get_default_password_validators
from django.core.exceptions import ValidationError
from approval.models import ApprovalRequest
from institute.models import Institute
from program.models import Standard
from student.models import StudentProfile, BoardOfEducation
from userprofile.models import UserProfile, ROLE_STUDENT, STATUS_UNAPPROVED, GENDER_CHOICES
from userprofile.decorators import admin_required


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
			if not request.POST.get("repeat_password"):
				return JsonResponse({"status": False, "msg": "Retype password can't be empty"})
			if request.POST.get("password") != request.POST.get("repeat_password"): 
				return JsonResponse({"status": False, "msg": "Password and retype password must be the same"})
			if request.POST.get("gender") not in [choice[0] for choice in GENDER_CHOICES]: 
				return JsonResponse({"status": False, "msg": "Invalid Gender Value"})
			if not request.POST.get("program_id"):
				return JsonResponse({"status": False, "msg": "Program ID shouldn't be empty"})
			if not request.POST.get("boe"):
				return JsonResponse({"status": False, "msg": "Board Of Education ID shouldn't be empty"})
			if not request.POST.get("standard_id"):
				return JsonResponse({"status": False, "msg": "Standard ID shouldn't be empty"})

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
				return JsonResponse({"status": False, "msg": "Internal Server Error 1"})

			userprofile = UserProfile()
			userprofile.user = user
			userprofile.role = ROLE_STUDENT
			userprofile.gender = request.POST.get("gender")
			userprofile.mobile = request.POST.get("mobile")
			userprofile.institute = institute
			userprofile.address = request.POST.get("address")
			userprofile.dob = datetime.now()
			userprofile.status = STATUS_UNAPPROVED

			studentprofile = StudentProfile()
			studentprofile.user = userprofile
			studentprofile.boe = BoardOfEducation.objects.get(boe_id = request.POST.get("boe"))
			studentprofile.standard = Standard.objects.get(standard_id = request.POST.get("standard_id"))
			studentprofile.roll_number = request.POST.get("roll_number")

			try:
				userprofile.save()
				userprofile.programs.add(request.POST.get("program_id"))
				studentprofile.save()
			except:
				user.delete()
				return JsonResponse({"status": False, "msg": "Internal Server Error 2"})

			registration_approval_request = ApprovalRequest(approval_type = APPROVAL_STUDENT_REGISTRATION, user = user)
			registration_approval_request.save()

			return JsonResponse({"status": True, "msg": "Registered Successfully"})
		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error 3"})


@csrf_exempt
@admin_required
def boe_create(request):
	if request.method == 'POST':

		try:
			if not request.POST.get("boe"):
				return JsonResponse({"status": False, "msg": "Boe Name shouldn't be empty"})

			if BoardOfEducation.objects.filter(boe_name = request.POST.get("boe")).exists():
				return JsonResponse({"status": False, "msg": "Boe Name already exists"})

			boe = BoardOfEducation()
			boe.boe_name = request.POST.get("boe")

			try:
				boe.save()
				return JsonResponse({"status": True, "msg": "Boe Added Successfully"})
			except:
				return JsonResponse({"status": False, "msg": "Internal Server Error"})

		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})