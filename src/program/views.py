import json

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from program.models import Program
from userprofile.decorators import admin_required

@csrf_exempt
@admin_required
def program_create(request):
	if request.method == 'POST':

		try:
			if not request.POST.get("program_name"):
				return JsonResponse({"status": False, "msg": "Program Name shouldn't be empty"})
			
			program = Program()
			program.program_name = request.POST.get("program_name")

			try:
				program.save()
				program.subjects.add(*map(int, json.loads(request.POST.get("subject_list"))["subject_list"]))
				return JsonResponse({"status": True, "msg": "Program Registered Successfully"})
			except:
				return JsonResponse({"status": False, "msg": "Internal Server Error"})

		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})
