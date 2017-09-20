import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from userprofile.decorators import admin_required
from userprofile.models import STATUS_APPROVED, STATUS_UNAPPROVED, ROLE_TEACHER, ROLE_STUDENT
from institute.models import Institute
from institute.models2 import InstituteAdmin
from student.models import StudentProfile
from teacher.models import TeacherProfile
from program.models import Program
from chapter.models import Subject
from userprofile.models import UserProfile
from datetime import datetime

@admin_required
@login_required(login_url='/login/')
def template_view_all_programs(request):
	if request.method == 'GET':
		resp = []
		for program in Program.objects.all():
			subject_list = []
			for subject in program.subjects.all():
				subject_list.append(subject.subject_name)

			odict={
				"program_id" : program.program_id,
				"program_name" : program.program_name,
				"subject_list" : subject_list
			}
			resp.append(odict)
	return render(request, 'adminportal/index.html', {'resp' : resp})


@admin_required
@login_required(login_url='/login/')
def template_view_all_subjects(request):
	if request.method == 'GET':
		resp = []
		for subject in Subject.objects.all():
			odict={
				"subject_id" : subject.subject_id,
				"subject_name" : subject.subject_name,
			}
			resp.append(odict)
	return render(request, 'adminportal/index.html', {'resp' : resp})


@admin_required
@login_required(login_url='/login/')
def template_view_all_institutes(request):
	if request.method == 'GET':
		resp = []
		for institute in Institute.objects.all():
			program_list = []
			for program in institute.programs.all():
				program_list.append(program.program_name)
			odict={
				"institute_id" : institute.institute_id,
				"institute_name" : institute.institute_name,
				"programs" : program_list,
				"address" : institute.address,
				"city" : institute.city,
				"state" : institute.state,
				"phone_no" : institute.phone_no,
				"manager_name" : institute.manager_name,
			}
			resp.append(odict)
	return render(request, 'adminportal/index.html', {'resp' : resp})

@admin_required
@login_required(login_url='/login/')
def template_view_all_institute_admins(request):
	if request.method == 'GET':
		resp = []
		for institute_admin in InstituteAdmin.objects.all():
			insti_list = []
			for institute in institute_admin.institutes.all():
				insti_list.append(institute.institute_name)
			odict={
				"institute_admin" : institute_admin.user,
				"institutes" : insti_list,
			}
			resp.append(odict)
	return render(request, 'adminportal/index.html', {'resp' : resp})


@csrf_exempt
@admin_required
@login_required(login_url='/login/')
def template_edit_program(request, id = "1"):
	if request.method == 'POST':

		try:
			if not request.POST.get("program_name"):
				return JsonResponse({"status": False, "msg": "Program Name shouldn't be empty"})

			if not request.POST.get("subject_list"):
				return JsonResponse({"status": False, "msg": "Subject List in Program shouldn't be empty"})

			subject_ids = json.loads(request.POST.get("subject_list"))["subject_list"]
			if not len(subject_ids)==len(Subject.objects.filter(pk__in = subject_ids)):
				return JsonResponse({"status": False, "msg": "Some of the Subject IDs are invalid or appear more than once"})
			
			program = Program.objects.get(program_id = id)
			program.program_name = request.POST.get("program_name")

			try:
				program.save()
				program.subjects.clear()
				program.subjects.add(*map(int, subject_ids))
				# return render(request, 'adminportal/index.html', {'resp' : 'Changes Saved Successfully'})
				return JsonResponse({"status": True, "msg": "Changes Saved Successfully"})
			except:
				return JsonResponse({"status": False, "msg": "Internal Server Error"})

		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})

@csrf_exempt
@admin_required
@login_required(login_url='/login/')
def template_edit_subject(request, id = "1"):
	if request.method == 'POST':

		try:
			if not request.POST.get("subject_name"):
				return JsonResponse({"status": False, "msg": "Subject Name shouldn't be empty"})
			
			subject = Subject.objects.get(subject_id = id)
			subject.subject_name = request.POST.get("subject_name")

			try:
				subject.save()
				# return render(request, 'adminportal/index.html', {'resp' : 'Changes Saved Successfully'})
				return JsonResponse({"status": True, "msg": "Changes Saved Successfully"})
			except:
				return JsonResponse({"status": False, "msg": "Internal Server Error"})

		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})

@csrf_exempt
@admin_required
@login_required(login_url='/login/')
def template_edit_institute(request, id = "1"):
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
			if not request.POST.get("program_list"):
				return JsonResponse({"status": False, "msg": "Program List in Institute shouldn't be empty"})

			program_ids = json.loads(request.POST.get("program_list"))["program_list"]
			if not len(program_ids)==len(Program.objects.filter(pk__in = program_ids)):
				return JsonResponse({"status": False, "msg": "Some of the Program IDs are invalid or appear more than once"})

			institute = Institute.objects.get(institute_id = id)
			institute.institute_name = request.POST.get("institute_name")
			institute.address = request.POST.get("address")
			institute.city = request.POST.get("city")
			institute.state = request.POST.get("state")
			institute.phone_no = request.POST.get("phone_no")
			institute.manager_name = request.POST.get("manager_name")

			try:
				institute.save()
				institute.programs.clear()
				institute.programs.add(*map(int, program_ids))
				# return render(request, 'adminportal/index.html', {'resp' : 'Changes Saved Successfully'})
				return JsonResponse({"status": True, "msg": "Changes Saved Successfully"})
			except:
				return JsonResponse({"status": False, "msg": "Internal Server Error"})

		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})

@csrf_exempt
@admin_required
@login_required(login_url='/login/')
def template_edit_institute_admin(request, id = "1"):
	if request.method == 'POST':

		try:
			if not request.POST.get("username"):
				return JsonResponse({"status": False, "msg": "Username shouldn't be empty"})
			if User.objects.filter(username = request.POST.get("username")).exists() and id != request.POST.get("username"):
				return JsonResponse({"status": False, "msg": "Given Username already in use"})

			user = User.objects.get(username = id)

			if User.objects.filter(email = request.POST.get("email")).exists() and user.email != request.POST.get("email"):
				return JsonResponse({"status": False, "msg": "Given email already in use"})
			if not request.POST.get("institute_list"):
				return JsonResponse({"status": False, "msg": "Institute List in InstituteAdmin shouldn't be empty"})

			institute_ids = json.loads(request.POST.get("institute_list"))["institute_list"]
			if not len(institute_ids)==len(Institute.objects.filter(pk__in = institute_ids)):
				return JsonResponse({"status": False, "msg": "Some of the Institute IDs are invalid or appear more than once"})
			
			instituteAdmin = InstituteAdmin.objects.get(user__user__username = id)	
			institute = None
			try:
				institute = Institute.objects.get(institute_id = request.POST.get("institute"))
			except:
				return JsonResponse({"status": False, "msg": "Given Institute Doesnt Exist"})

			user.username = request.POST.get("username")
			user.first_name = request.POST.get("firstname")
			user.last_name = request.POST.get("lastname")
			user.email = request.POST.get("email")

			try:
				user.save()
			except:
				return JsonResponse({"status": False, "msg": "Internal Server Error"})

			userprofile = UserProfile.objects.get(user__username = id)
			userprofile.user = user
			userprofile.gender = request.POST.get("gender")
			userprofile.mobile = request.POST.get("mobile")
			userprofile.institute = institute
			userprofile.dob = datetime.now()

			instituteAdmin.user = userprofile

			try:
				userprofile.save()
				instituteAdmin.save()
				instituteAdmin.institutes.clear()
				instituteAdmin.institutes.add(*map(int, institute_ids))
			except:
				user.delete()
				return JsonResponse({"status": False, "msg": "Internal Server Error"})

			# return render(request, 'adminportal/index.html', {'resp' : 'Changes Saved Successfully'})
			return JsonResponse({"status": True, "msg": "Changes Saved Successfully"})

		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})


@csrf_exempt
@admin_required
@login_required(login_url='/login/')
def template_delete_program(request, id = "1"):
	if request.method == 'POST':

		try:
					
			program = Program.objects.get(program_id = id)
			program.delete()
			# return render(request, 'adminportal/index.html', {'resp' : 'Changes Saved Successfully'})
			return JsonResponse({"status": True, "msg": "Deleted Successfully"})

		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})

@csrf_exempt
@admin_required
@login_required(login_url='/login/')
def template_delete_subject(request, id = "1"):
	if request.method == 'POST':

		try:
					
			subject = Subject.objects.get(subject_id = id)
			subject.delete()
			# return render(request, 'adminportal/index.html', {'resp' : 'Changes Saved Successfully'})
			return JsonResponse({"status": True, "msg": "Deleted Successfully"})

		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})
