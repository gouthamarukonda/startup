import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portal.settings.localsettings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import numpy as np

from datetime import datetime
from django.contrib.auth.models import User
from answer.models import Answer
from chapter.models import Chapter, SUBJECT_CHOICES, Subject
from institute.models import Institute
from paper.models import Paper, Mapping
from question.models import Question
from student.models import StudentProfile, STD_CHOICES
from teacher.models import TeacherProfile
from userprofile.models import UserProfile, ROLE_STUDENT, STATUS_APPROVED, ROLE_TEACHER
from answer.tools  import evaluate_answer
from program.models import Program

# Create superuser

superuser = User(username = "admin")
superuser.set_password("admin12345")
superuser.is_superuser = True
superuser.is_staff = True
superuser.is_active = True
superuser.save()

#create programs

programs = ['JEE ADV', 'JEE MAINS', 'AIIMS', 'NEET']

for p in programs:
	program = Program()
	program.program_name = p
	program.save()


#create institutes

sample_institute_ids = ['powai', 'hyd', 'vizag']

for cid in sample_institute_ids:
	institute = Institute()
	institute.institute_name = cid
	institute.address = cid
	institute.city = cid
	institute.state = "AP"
	institute.phone_no = "123456"
	institute.manager_name = "avinash"
	institute.save()


# Create users for student, teacher

sample_student_ids = ['10001', '10002', '10003', '10004', '10005']
sample_teacher_ids = ['20001', '20002', '20003', '20004', '20005']

for cid in sample_student_ids:
	user = User(username = cid)
	user.set_password(cid)
	user.first_name = "CUSTOMER-" + cid[0] + cid[4]
	user.email = "CUSTOMER-" + cid[0] + cid[4] + "@gmail.com"
	user.is_active = True
	user.save()
	userprofile = UserProfile()
	userprofile.user = user
	userprofile.role = ROLE_STUDENT
	userprofile.mobile = cid + "000000"
	np.random.shuffle(sample_institute_ids)
	userprofile.institute = Institute.objects.get(institute_name = sample_institute_ids[0])
	userprofile.dob = datetime.now()
	userprofile.status = STATUS_APPROVED
	userprofile.save()
	studentprofile = StudentProfile()
	studentprofile.user = userprofile
	studentprofile.boe = "CBSE"
	studentprofile.standard = '2'
	studentprofile.save()

for cid in sample_teacher_ids:
	user = User(username = cid)
	user.set_password(cid)
	user.first_name = "CUSTOMER-" + cid[0] + cid[4]
	user.email = "CUSTOMER-" + cid[0] + cid[4] + "@gmail.com"
	user.is_active = True
	user.save()
	userprofile = UserProfile()
	userprofile.user = user
	userprofile.role = ROLE_TEACHER
	userprofile.mobile = cid + "000000"
	np.random.shuffle(sample_institute_ids)
	userprofile.institute = Institute.objects.get(institute_name = sample_institute_ids[0])
	userprofile.dob = datetime.now()
	userprofile.status = STATUS_APPROVED
	userprofile.save()
	teacherprofile = TeacherProfile()
	teacherprofile.user = userprofile
	teacherprofile.experience = "2"
	teacherprofile.save()


#create subjects

subjects = ['maths', 'physics', 'chemistry', 'zoology', 'botany', 'GK']

for sub in subjects:
	new_sub = Subject()
	new_sub.subject_name = sub
	new_sub.save()


# create chapters

sample_chapter_maths = ['limits', 'differentiation', 'continuity', 'coordinate geometry', 'integration']
sample_chapter_physics = ['electricity', 'magnetism', 'light', 'Force', 'units and measurement']
sample_chapter_chemistry = ['acids and bases', 'stochiometry', 'organic', 'inorganic', 'periodic elements']
subjects = ['1', '2', '3', '4', '5', '6']

for cid in subjects:
	temp = sample_chapter_maths
	if cid == '0':
		temp = sample_chapter_maths
	if cid == '1':
		temp = sample_chapter_physics
	if cid == '2':
		temp = sample_chapter_chemistry
	for i in range(5):
		chapter = Chapter()
		chapter.chapter_name = temp[i]
		chapter.subject = Subject.objects.get(subject_id = int(cid))
		chapter.save()


# create papers

PM = ['0', '1']
Paper_type = ['0', '1']
Paper_name = ['DPP1', 'DPP2', 'Exam1', 'Exam2', 'Exam3']
count = 0
for name in Paper_name:
	paper = Paper()
	paper.program = Program.objects.get(program_id = (count % 4) + 1)
	paper.paper_name = name
	paper.paper_type = Paper_type[count % 2]
	paper.teacher_id = TeacherProfile.objects.get(user__user__username = sample_teacher_ids[count % 5])
	paper.start_time = datetime.now()
	paper.end_time = datetime.now()
	paper.partial_marking = PM[count % 2]
	count = count + 1
	paper.save()


# create question

Q_type = ['0', '1', '2', '3']
complexity = ['0', '1', '2', '3', '4']
sample_question = ['if A=90 deg , then sinA= ?', 'if A=90 deg , then cosA= ?', 'if A=90 deg , then tanA= ?', 'if A=90 deg , then cotA= ?', 'if A=90 deg , then secA= ?']
sample_solution = [0,1,2,3,4]
count = 1
for i in sample_question:
	question = Question()
	question.chapter = Chapter.objects.get(chapter_id = count)
	question.question_type = Q_type[count % 4]
	question.question = i
	question.solution = sample_solution[count % 4]
	question.complexity = complexity[count % 5]
	question.teacher = TeacherProfile.objects.get(user__user__username = sample_teacher_ids[count % 5])
	question.marks_positive = 5
	question.marks_negative = -5
	count = count + 1
	if question.question_type == '3':
		question.int_answer = sample_solution[count % 5]
	elif question.question_type == '0':
		question.options =  [["A", "0", "0"], ["B", "1", "1"], ["C", "1", "2"], ["D", "0", "3"]]
	else:
		question.options =  [["A", "0", "0"], ["B", "0", "1"], ["C", "1", "2"], ["D", "0", "3"]]
	question.save()
	mapping = Mapping()
	mapping.paper = Paper.objects.get(paper_name = Paper_name[count % 5])
	mapping.question = question
	mapping.save()

for i in sample_question:
	question = Question()
	question.chapter = Chapter.objects.get(chapter_name = sample_chapter_physics[count % 5])
	question.question_type = Q_type[count % 4]
	question.question = i
	question.solution = sample_solution[count % 4]
	question.complexity = complexity[count % 5]
	question.teacher = TeacherProfile.objects.get(user__user__username = sample_teacher_ids[count % 5])
	question.marks_positive = 5
	question.marks_negative = -5
	count = count + 1
	if question.question_type == '3':
		question.int_answer = sample_solution[count % 5]
	elif question.question_type == '0':
		question.options =  [["A", "1", "0"], ["B", "1", "1"], ["C", "1", "2"], ["D", "0", "3"]]
	else:
		question.options =  [["A", "0", "0"], ["B", "0", "1"], ["C", "1", "2"], ["D", "0", "3"]]
	question.save()
	mapping = Mapping()
	mapping.paper = Paper.objects.get(paper_name = Paper_name[count % 5])
	mapping.question = question
	mapping.save()

for i in sample_question:
	question = Question()
	question.chapter = Chapter.objects.get(chapter_name = sample_chapter_chemistry[count % 5])
	question.question_type = Q_type[count % 4]
	question.question = i
	question.solution = sample_solution[count % 4]
	question.complexity = complexity[count % 5]
	question.teacher = TeacherProfile.objects.get(user__user__username = sample_teacher_ids[count % 5])
	question.marks_positive = 5
	question.marks_negative = -5
	count = count + 1
	if question.question_type == '3':
		question.int_answer = sample_solution[count % 5]
	elif question.question_type == '0':
		question.options =  [["A", "0", "0"], ["B", "1", "1"], ["C", "1", "2"], ["D", "0", "3"]]
	else:
		question.options =  [["A", "0", "0"], ["B", "1", "1"], ["C", "0", "2"], ["D", "0", "3"]]
	question.save()
	mapping = Mapping()
	mapping.paper = Paper.objects.get(paper_name = Paper_name[count % 5])
	mapping.question = question
	mapping.save()

# create answer

for i in range(1,16):
	mapping = Mapping.objects.get(map_id = i)
	answer = Answer(user = User.objects.get(username = sample_student_ids[count % 5]), mapping = mapping)

	if mapping.question.question_type == '3':
		answer.int_answer = sample_solution[count % 5]
	elif mapping.question.question_type == '0':
		answer.answer_array = ['C']
	else:
		answer.answer_array = ['C']
	answer.time_taken += int(count)
	answer.marks_obtained = evaluate_answer(mapping.paper, mapping.question, answer)
	answer.save()
	count = count + 1