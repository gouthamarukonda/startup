from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import ApprovalRequest, STATUS_WAITING
from userprofile.decorators import admin_required

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
			if not request.POST.get("approval_id"):
				return JsonResponse({"status": False, "msg": "approval_id required"})

			if not ApprovalRequest.objects.filter(approval_id = request.POST.get("approval_id")).exists():
				return JsonResponse({"status": False, "msg": "approval_id doesn't exist"})

			if not request.POST.get("action"):
				return JsonResponse({"status": False, "msg": "action required"})

			approvalRequest = ApprovalRequest.objects.get(approval_id = request.POST.get("approval_id"))
			approvalRequest.status = request.POST.get("action")
			approvalRequest.save()
			return JsonResponse({"status": True, "msg": "Status updated successfully"})

		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})
