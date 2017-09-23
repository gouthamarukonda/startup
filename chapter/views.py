from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from chapter.models import Chapter, Subject
from userprofile.decorators import teacher_required, admin_required

@csrf_exempt
@teacher_required
def chapter_create(request):
	if request.method == 'POST':

		try:
			if not request.POST.get("chapter_name"):
				return JsonResponse({"status": False, "msg": "Chapter Name shouldn't be empty"})

			if not Subject.objects.filter(subject_id = int(request.POST.get("subject"))).exists(): 
				return JsonResponse({"status": False, "msg": "Invalid Subject"})
			
			chapter = Chapter()
			chapter.chapter_name = request.POST.get("chapter_name")
			chapter.subject = Subject.objects.get(subject_id = request.POST.get("subject"))

			try:
				chapter.save()
				return JsonResponse({"status": True, "msg": "Chapter created Successfully"})
			except:
				return JsonResponse({"status": False, "msg": "Internal Server Error"})

		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})

@csrf_exempt
@admin_required
def subject_create(request):
	if request.method == 'POST':

		try:
			if not request.POST.get("subject_name"):
				return JsonResponse({"status": False, "msg": "Subject Name shouldn't be empty"})

			if Subject.objects.filter(subject_name = request.POST.get("subject_name")).exists():
				return JsonResponse({"status": False, "msg": "Subject already exists"})
			
			subject = Subject()
			subject.subject_name = request.POST.get("subject_name")

			try:
				subject.save()
				return JsonResponse({"status": True, "msg": "Subject created Successfully"})
			except:
				return JsonResponse({"status": False, "msg": "Internal Server Error"})

		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})
