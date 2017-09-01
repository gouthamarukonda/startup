from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.dateparse import parse_datetime
from datetime import datetime
from django.contrib.admin.views.decorators import staff_member_required

from paper.models import Paper, PM_CHOICES, PAPER_CHOICES
from userprofile.decorators import teacher_required

@csrf_exempt
@teacher_required
def paper_create(request):
	if request.method == 'POST':

		try:
			if not request.POST.get("paper_name"):
				return JsonResponse({"status": False, "msg": "Paper Name shouldn't be empty"})
			
			if request.POST.get("paper_type") not in [choice[0] for choice in PAPER_CHOICES]: 
				return JsonResponse({"status": False, "msg": "Invalid Paper Type"})

			if request.POST.get("partial_marking") not in [choice[0] for choice in PM_CHOICES]: 
				return JsonResponse({"status": False, "msg": "Invalid Partial Marking Scheme"})
			
			paper = Paper()
			paper.paper_name = request.POST.get("paper_name")
			paper.paper_type = request.POST.get("paper_type")
			paper.teacher_id = request.user.userprofile.teacherprofile
			paper.start_time = datetime.now()
			paper.end_time = datetime.now()
			paper.partial_marking = request.POST.get("partial_marking")

			try:
				paper.save()
				return JsonResponse({"status": True, "msg": "Paper Registered Successfully"})
			except:
				return JsonResponse({"status": False, "msg": "Internal Server Error"})

		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})
