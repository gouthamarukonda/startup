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

# Programs
@admin_required
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
				"subject_list" : subject_list,
			}
			resp.append(odict)
		return render(request, 'adminportal/programs/view-programs.html', {'resp' : resp})

@csrf_exempt
@admin_required
def template_edit_program(request, id):
	if request.method == 'GET':
		if not Program.objects.filter(program_id = id).exists():
			return render(request, 'adminportal/programs/edit-program.html', {'resp' : "Program ID doesn't exists", 'status' : False})
		program = Program.objects.get(program_id = id)
		subject_list = []
		all_subjects = []
		for subject in program.subjects.all():
			subject_list.append((subject.subject_id, subject.subject_name))
		for subject in Subject.objects.all():
			all_subjects.append((subject.subject_id, subject.subject_name))
		subject_complement_list = list(set(all_subjects) - set(subject_list))
		program={
			"program_id" : program.program_id,
			"program_name" : program.program_name,
			"subject_list" : subject_list,
			"subject_complement_list" : subject_complement_list,
			}
		return render(request, 'adminportal/programs/edit-program.html', {'program' : program, 'status' : True})


@csrf_exempt
@admin_required
def template_delete_program(request):
	if request.method == 'POST':
		try:
			if not request.POST.get("program_id"):
				return JsonResponse({"status": False, "msg": "Program ID shouldn't be empty"})

			if not Program.objects.filter(program_id = request.POST.get("program_id")).exists():
				return JsonResponse({"status": False, "msg": "Given Program ID doesn't exist, Please refresh the page"})

			program = Program.objects.get(program_id = request.POST.get("program_id"))
			program.delete()
			return JsonResponse({"status": True, "msg": "Deleted Successfully"})
		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})

@csrf_exempt
@admin_required
def template_update_program(request):
	if request.method == 'POST':
		try:
			if not request.POST.get("program_id"):
				return JsonResponse({"status": False, "msg": "Program ID shouldn't be empty"})

			if not request.POST.get("program_name"):
				return JsonResponse({"status": False, "msg": "Program Name shouldn't be empty"})

			if not request.POST.get("subject_list"):
				return JsonResponse({"status": False, "msg": "Subject List in Program shouldn't be empty"})

			subject_ids = request.POST.getlist("subject_list")
			if not len(subject_ids)==len(Subject.objects.filter(pk__in = subject_ids)):
				return JsonResponse({"status": False, "msg": "Some of the Subject IDs are invalid or appear more than once"})

			program = Program.objects.get(program_id = request.POST.get("program_id"))
			program.program_name = request.POST.get("program_name")

			try:
				program.save()
				program.subjects.clear()
				program.subjects.add(*map(int, subject_ids))
				return JsonResponse({"status": True, "msg": "Changes Saved Successfully"})
			except:
				return JsonResponse({"status": False, "msg": "Internal Server Error"})
		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})

@csrf_exempt
@admin_required
def template_add_program(request):
	if request.method == 'GET':
		resp = []
		for subject in Subject.objects.all():
			odict={
				"subject_id" : subject.subject_id,
				"subject_name" : subject.subject_name,
			}
			resp.append(odict)
		return render(request, 'adminportal/programs/add-program.html', {'resp' : resp})




# Subjects
@admin_required
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

@csrf_exempt
@admin_required
def template_edit_subject(request, id):
	if request.method == 'GET':
		if not Subject.objects.filter(subject_id = id).exists():
			return render(request, 'adminportal/index.html', {'resp' : "Subject ID doesn't exists", 'status' : False})
		subject = Subject.objects.get(subject_id = id)
		resp = []
		odict={
			"subject_id" : subject.subject_id,
			"subject_name" : subject.subject_name,
		}
		resp.append(odict)
		return render(request, 'adminportal/index.html', {'resp' : resp, 'status' : True})

@csrf_exempt
@admin_required
def template_delete_subject(request):
	if request.method == 'POST':
		try:
			if not request.POST.get("subject_id"):
				return JsonResponse({"status": False, "msg": "Subject ID shouldn't be empty"})

			if not Subject.objects.filter(subject_id = request.POST.get("subject_id")).exists():
				return JsonResponse({"status": False, "msg": "Given Subject ID doesn't exist"})

			subject = Subject.objects.get(subject_id = request.POST.get("subject_id"))
			subject.delete()
			return JsonResponse({"status": True, "msg": "Deleted Successfully"})
		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})

@csrf_exempt
@admin_required
def template_update_subject(request):
	if request.method == 'POST':
		try:
			if not request.POST.get("subject_name"):
				return JsonResponse({"status": False, "msg": "Subject Name shouldn't be empty"})

			subject = Subject.objects.get(subject_id=id)
			subject.subject_name = request.POST.get("subject_name")
			try:
				subject.save()
				return JsonResponse({"status": True, "msg": "Changes Saved Successfully"})
			except:
				return JsonResponse({"status": False, "msg": "Internal Server Error"})
		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})




# Institutes
@admin_required
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

@csrf_exempt
@admin_required
def template_edit_institute(request, id):
	if request.method == 'GET':
		if not Institute.objects.filter(institute_id = id).exists():
			return render(request, 'adminportal/index.html', {'resp' : "Institute ID doesn't exists", 'status' : False})
		institute = Institute.objects.get(institute_id = id)
		resp = []
		program_list = []
		all_programs = []
		for program in institute.programs.all():
			program_list.append((program.program_id, program.program_name))
		for program in Program.objects.all():
			all_programs.append((program.program_id, program.program_name))
		program_complement_list = list(set(all_programs) - set(program_list))
		odict={
			"institute_id" : institute.institute_id,
			"institute_name" : institute.institute_name,
			"programs" : program_list,
			"address" : institute.address,
			"city" : institute.city,
			"state" : institute.state,
			"phone_no" : institute.phone_no,
			"manager_name" : institute.manager_name,
			"program_complement_list" : program_complement_list,
		}
		resp.append(odict)
		return render(request, 'adminportal/index.html', {'resp' : resp, 'status' : True})

@csrf_exempt
@admin_required
def template_delete_institute(request):
	if request.method == 'POST':
		try:
			if not request.POST.get("institute_id"):
				return JsonResponse({"status": False, "msg": "Institute ID shouldn't be empty"})

			if not Institute.objects.filter(institute_id = request.POST.get("institute_id")).exists():
				return JsonResponse({"status": False, "msg": "Given Institute ID doesn't exist"})

			institute = Institute.objects.get(institute_id = request.POST.get("institute_id"))
			institute.delete()
			return JsonResponse({"status": True, "msg": "Deleted Successfully"})
		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})

@csrf_exempt
@admin_required
def template_update_institute(request):
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
				return JsonResponse({"status": True, "msg": "Changes Saved Successfully"})
			except:
				return JsonResponse({"status": False, "msg": "Internal Server Error"})
		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})





# Institute Admins
@admin_required
def template_view_all_institute_admins(request):
	if request.method == 'GET':
		resp = []
		for institute_admin in InstituteAdmin.objects.all():
			insti_list = []
			for institute in institute_admin.institutes.all():
				insti_list.append(institute.institute_name)
			insti_list.append(institute_admin.user.institute.institute_name)
			insti_list = list(set(insti_list))
			odict={
				"institute_admin_id" : institute_admin.user.user.username,
				"institute_admin_name" : institute_admin.user.user.first_name + " " + 
										institute_admin.user.user.last_name,
				"institutes" : insti_list,
			}
			resp.append(odict)
		return render(request, 'adminportal/index.html', {'resp' : resp})

@csrf_exempt
@admin_required
def template_edit_institute_admin(request, id):
	if request.method == 'GET':
		if not InstituteAdmin.objects.filter(user__user__username = id).exists():
			return render(request, 'adminportal/index.html', {'resp' : "Institute Admin ID doesn't exists", 'status' : False})

		institute_admin = InstituteAdmin.objects.get(user__user__username = id)
		resp = []
		insti_list = []
		all_insti = []
		for institute in institute_admin.institutes.all():
			insti_list.append((institute.institute_id, institute.institute_name))
		for institute in Institute.objects.all():
			all_insti.append((institute.institute_id, institute.institute_name))
		institute_complement_list = list(set(all_insti) - set(insti_list))
		odict={
			"username" : institute_admin.user.user.username,
			"firstname" : institute_admin.user.user.first_name,
			"lastname" : institute_admin.user.user.last_name,
			"email" : institute_admin.user.address,
			"gender" : institute_admin.user.gender,
			"mobile" : institute_admin.user.mobile,
			"dob" : institute_admin.user.dob,
			"main_institute" : institute_admin.user.institute,
			"institutes" : insti_list,
			"institute_complement_list" : institute_complement_list,
		}
		resp.append(odict)
		return render(request, 'adminportal/index.html', {'resp' : resp, 'status' : True})


@csrf_exempt
@admin_required
def template_delete_institute_admin(request):
	if request.method == 'POST':
		try:
			if not request.POST.get("institute_admin_id"):
				return JsonResponse({"status": False, "msg": "Institute Admin ID shouldn't be empty"})

			if not InstituteAdmin.objects.filter(user__user__username = request.POST.get("institute_admin_id")).exists():
				return JsonResponse({"status": False, "msg": "Given InstituteAdmin ID doesn't exist"})

			institute_admin = InstituteAdmin.objects.get(user__user__username = request.POST.get("institute_admin_id"))
			userprofile = institute_admin.user
			user = userprofile.user
			user.delete()
			userprofile.delete()
			institute_admin.delete()
			return JsonResponse({"status": True, "msg": "Deleted Successfully"})
		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})

@csrf_exempt
@admin_required
def template_update_institute_admin(request):
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
			userprofile.dob = request.POST.get("dob")

			instituteAdmin.user = userprofile

			try:
				userprofile.save()
				instituteAdmin.save()
				instituteAdmin.institutes.clear()
				instituteAdmin.institutes.add(*map(int, institute_ids))
			except:
				return JsonResponse({"status": False, "msg": "Internal Server Error"})
			
			return JsonResponse({"status": True, "msg": "Changes Saved Successfully"})
		except:
			return JsonResponse({"status": False, "msg": "Internal Server Error"})