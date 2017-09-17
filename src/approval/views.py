from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import ApprovalRequest, STATUS_WAITING, STATUS_APPROVED
from .approvalFuncs import *
from userprofile.decorators import admin_required


ApprovalFunctions = {}
ApprovalFunctions[APPROVAL_STUDENT_REGISTRATION] = approve_registration
ApprovalFunctions[APPROVAL_TEACHER_REGISTRATION] = approve_registration
# ApprovalFunctions[APPROVAL_STUDENT_ADD_PROGRAM] = None
# ApprovalFunctions[APPROVAL_TEACHER_ADD_PROGRAM] = None
# ApprovalFunctions[APPROVAL_PASSWORD_RESET] = None


@csrf_exempt
@login_required(login_url='/login/')
def submit_approval_request(request):
	if request.method == 'POST':

		try:
			if not request.POST.get("approval_type"):
				return JsonResponse({"status": False, "msg": "approval_type required"})

			approvalRequest = ApprovalRequest()
			approvalRequest.approval_type = request.POST.get("approval_type")
			approvalRequest.user = request.user
			approvalRequest.status = STATUS_WAITING

			if request.POST.get("data"):
				approvalRequest.data = request.POST.get("data")

			approvalRequest.save()
			return JsonResponse({"status": True, "msg": "Approval Request Created"})

		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})

@csrf_exempt
@admin_required
def update_status(request):
	if request.method == 'POST':

		try:
			if not request.POST.get("approval_request_id"):
				return JsonResponse({"status": False, "msg": "approval_request_id required"})

			if not ApprovalRequest.objects.filter(approval_request_id = request.POST.get("approval_request_id")).exists():
				return JsonResponse({"status": False, "msg": "approval_request_id doesn't exist"})

			approvalRequest = ApprovalRequest.objects.get(approval_request_id = request.POST.get("approval_request_id"))

			retval = None
			if request.POST.get("action") == STATUS_APPROVED:
				if approvalRequest.approval_type not in ApprovalFunctions:
					return JsonResponse({"status": False, "msg": "Approval Function not defined for approval_type"})
				retval = ApprovalFunctions[approvalRequest.approval_type](approvalRequest)
			if retval is not None:
				return retval

			approvalRequest.status = request.POST.get("action")
			approvalRequest.save()
			return JsonResponse({"status": True, "msg": "Status updated successfully"})

		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})

@csrf_exempt
@admin_required
def update_comment(request):
	if request.method == 'POST':

		try:
			if not request.POST.get("approval_request_id"):
				return JsonResponse({"status": False, "msg": "approval_request_id required"})

			if not ApprovalRequest.objects.filter(approval_request_id = request.POST.get("approval_request_id")).exists():
				return JsonResponse({"status": False, "msg": "approval_request_id doesn't exist"})

			if not request.POST.get("comment"):
				return JsonResponse({"status": False, "msg": "comment required"})

			approvalRequest = ApprovalRequest.objects.get(approval_request_id = request.POST.get("approval_request_id"))
			approvalRequest.comment = request.POST.get("comment")
			approvalRequest.save()
			return JsonResponse({"status": True, "msg": "Comment updated successfully"})

		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})
