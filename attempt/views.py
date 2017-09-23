from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from userprofile.decorators import student_required

from .models import Attempt
from paper.models import Paper

@csrf_exempt
@student_required
def register_attempt(request):
	if request.method == 'POST':

		try:
			if not Paper.objects.filter(paper_id = request.POST.get("paper_id")).exists():
				return JsonResponse({"status": False, "msg": "Paper ID doesn't exist"})

			attempt = Attempt()
			attempt.user = request.user
			attempt.paper = Paper.objects.get(paper_id = request.POST.get("paper_id"))
			attempt.status = request.POST.get("status")
			attempt.start_time = datetime.now()
			attempt.end_time = datetime.now()
			attempt.save()
			return JsonResponse({"status": True, "msg": "Attempt registered successfully"})

		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})
