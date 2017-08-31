from django.shortcuts import render

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.dateparse import parse_datetime
from datetime import datetime


from userprofile.models import STATUS_APPROVED, STATUS_UNAPPROVED

@csrf_exempt
@staff_member_required
def user_approve(request):
	if request.method == 'POST':
		try:
			if not request.POST.get("username"):
				return JsonResponse({"status": False, "msg": "User ID shouldn't be empty"})
			else:
				if User.objects.filter(username = request.POST.get("username")).exists():
					user = User.objects.get(username = request.POST.get("username"))
					user.is_active = True
					user.userprofile__status = STATUS_APPROVED
					user.save()
					return JsonResponse({"status": True, "msg": "User Approved Sucessfully"})
				else:
					return JsonResponse({"status": False, "msg": "User Doesn't exist"})
		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})




@csrf_exempt
@staff_member_required
def user_disapprove(request):
	if request.method == 'POST':
		try:
			if not request.POST.get("username"):
				return JsonResponse({"status": False, "msg": "User ID shouldn't be empty"})
			else:
				if User.objects.filter(username = request.POST.get("username")).exists():
					user = User.objects.get(username = request.POST.get("username"))
					user.is_active = False
					user.userprofile__status = STATUS_UNAPPROVED
					user.save()
					return JsonResponse({"status": True, "msg": "User DisApproved Sucessfully"})
				else:
					return JsonResponse({"status": False, "msg": "User Doesn't exist"})

		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})