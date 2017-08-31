from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from chapter.models import Chapter, SUBJECT_CHOICES
from userprofile.decorators import teacher_required

@csrf_exempt
@teacher_required
def chapter_create(request):
	if request.method == 'POST':

		try:
			if not request.POST.get("chapter_name"):
				return JsonResponse({"status": False, "msg": "Chapter Name shouldn't be empty"})
			
			if request.POST.get("subject") not in [choice[0] for choice in SUBJECT_CHOICES]: 
				return JsonResponse({"status": False, "msg": "Invalid Subject"})
			
			chapter = Chapter()
			chapter.chapter_name = request.POST.get("chapter_name")
			chapter.subject = request.POST.get("subject")

			try:
				chapter.save()
				return JsonResponse({"status": True, "msg": "Chapter created Successfully"})
			except:
				return JsonResponse({"status": False, "msg": "Internal Server Error"})

		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})
