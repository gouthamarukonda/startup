from django.shortcuts import render

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.dateparse import parse_datetime
from datetime import datetime
from django.contrib.admin.views.decorators import staff_member_required

from institute.models import Institute

@csrf_exempt
@staff_member_required	
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

			institute = Institute()
			institute.institute_name = request.POST.get("institute_name")
			institute.address = request.POST.get("address")
			institute.city = request.POST.get("city")
			institute.state = request.POST.get("state")
			institute.phone_no = request.POST.get("phone_no")
			institute.manager_name = request.POST.get("manager_name")

			try:
				institute.save()
				return JsonResponse({"status": True, "msg": "Institute Registered Successfully"})
			except:
				return JsonResponse({"status": False, "msg": "Internal Server Error"})

		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})
