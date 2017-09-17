from django.http import JsonResponse
from .approvalTypes import *
from userprofile.models import STATUS_APPROVED
from django.contrib.auth.models import User

def approve_registration(approvalRequest):

	try:
		user = approvalRequest.user
		user.userprofile.status = STATUS_APPROVED
		user.userprofile.save()
		user.save()
		return None
	except:
		return JsonResponse({"status": False, "msg": "Internal Server Error"})
