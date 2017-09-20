import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portal.settings.localsettings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import numpy as np

from datetime import datetime
from datetime import timedelta
from django.contrib.auth.models import User
from answer.models import Answer
from chapter.models import Chapter, Subject
from institute.models import Institute
from institute.models2 import InstituteAdmin
from paper.models import Paper, PaperType
from question.models import Question
from student.models import StudentProfile, BoardOfEducation
from teacher.models import TeacherProfile
from userprofile.models import UserProfile, ROLE_STUDENT, STATUS_APPROVED, ROLE_TEACHER, ROLE_INSTITUTE_ADMIN
from answer.tools  import evaluate_answer
from program.models import Program, Standard
from attempt.models import Attempt
from answer.tools import evaluate_answer

# Create superuser

superuser = User(username = "admin")
superuser.set_password("admin12345")
superuser.email="admin@admin.com"
superuser.first_name = "Admin"
superuser.last_name	= "Admin"
superuser.is_superuser = True
superuser.is_staff = True
superuser.is_active = True
superuser.save()


# create boards of education

boards = [
'Central Board of Secondary Education (CBSE)',
'National Institute of Open Schooling (NIOS)',
'Council for the Indian School Certificate Examinations (CISCE)',
'Grameen Mukt Vidhyalayi Shiksha Sansthan(GMVSS)',
'Andhra Pradesh Board of Secondary Education',
'Andhra Pradesh Open School Society',
'Assam Board of Secondary Education',
'Assam Higher Secondary Education Council',
'Assam State Open School',
'Bihar Board of Open Schooling & Examinations',
'Bihar School Examination Board',
'Uttar Pradesh Board of High School and Intermediate Education Allahabad',
'Madhya Pradesh Board of Secondary Education (Gwalior)',
'Madhya Pradesh Board of Secondary Education',
'Madhya Pradesh State Open School',
'Rajasthan Board of Secondary Education',
'Rajasthan State Open School',
'Chhattisgarh Board of Education',
'Central Board of Secondary Education (CBSE)',
'Council for the Indian School Certificate Examinations (CISCE)',
'Goa Board of Secondary & Higher Secondary Education',
'Gujarat Secondary Education Board',
'[[Gujarat state open school|Gujarat State Open School]',
'Haryana Board of School Education',
'Haryana State Open School',
'Himachal Pradesh Board of School Education',
'Himachal Pradesh State Open School',
'Jharkhand Academic Council',
'Jharkhand State Open School, Ranchi.',
'Jammu and Kashmir State Board of School Education',
'Jammu and Kashmir State Open School',
'Karnataka Secondary Education Examination Board',
'Karnataka State Open School',
'Kerala Higher Secondary Examination Board',
'Kerala State Open School',
'Maharashtra State Board of Secondary and Higher Secondary Education',
'Meghalaya Board of School Education',
'Mizoram Board of School Education',
'Nagaland Board of School Education',
'National Institute of Open Schooling',
'Orissa Board of Secondary Education',
'Orissa Council of Higher Secondary Education',
'Punjab School Education Board',
'Tamil Nadu Board of Secondary Education',
'Tripura Board of Secondary Education',
'Telangana Board of Intermediate Education',
'Telangana Board of Secondary Education',
'Uttarakhand Board of School Education',
'West Bengal Board of Madrasah Education',
'West Bengal Board of Primary Education',
'West Bengal Board of Secondary Education',
'West Bengal Council of Higher Secondary Education',
'West Bengal Council of Rabindra Open Schooling',
'West Bengal State Council of Vocational Education']

for board in boards:
	boe = BoardOfEducation()
	boe.boe_name = board
	boe.save()


# create standards

standards = ['8', '9', '10', '11', '12']

for i in standards:
	standard = Standard()
	standard.standard_name = i
	standard.save()


#create subjects

subjects = ['maths', 'physics', 'chemistry', 'botany', 'zoology', 'GK']

for sub in subjects:
	new_sub = Subject()
	new_sub.subject_name = sub
	new_sub.save()


#create programs

programs = ['JEE ADV', 'JEE MAINS', 'AIIMS', 'NEET', 'AFMC', 'NDA']
count = 1

for p in programs:
	program = Program()
	program.program_name = p
	program.save()
	program.subjects.add((count%6)+1, ((count+1)%6)+1, ((count+2)%6)+1, ((count+3)%6)+1)
	count += 1


#create institutes

sample_institute_ids = ['powai', 'hyd', 'vizag', 'pune', 'delhi', 'madras', 'kgp']
count = 1

for cid in sample_institute_ids:
	institute = Institute()
	institute.institute_name = cid
	institute.address = cid
	institute.city = cid
	institute.state = "AP"
	institute.phone_no = "123456"
	institute.manager_name = "avinash"
	institute.save()
	institute.programs.add((count%6)+1, ((count+1)%6)+1, ((count+2)%6)+1, ((count+3)%6)+1)
	count += 1


# create Paper Types

paper_types = ['DPP', 'Exam', 'AIST', 'AIFT', 'SAT', 'FAT', 'CQ']

for p in paper_types:
	paper_type = PaperType()
	paper_type.type_name = p
	paper_type.save()


# Create users for student, teacher, institute Admin

sample_student_ids = ['10001', '10002', '10003', '10004', '10005']
sample_teacher_ids = ['20001', '20002', '20003', '20004', '20005']
sample_insti_admin_ids = ['30001', '30002', '30003', '30004', '30005']
count = 0

for cid in sample_student_ids:
	np.random.shuffle(sample_institute_ids)
	user = User(username = cid)
	user.set_password(cid+cid)
	user.first_name = "CUSTOMER-" + cid[0] + cid[4]
	user.last_name = "student"
	user.email = "CUSTOMER-" + cid[0] + cid[4] + "@gmail.com"
	user.save()
	userprofile = UserProfile()
	userprofile.user = user
	userprofile.role = ROLE_STUDENT
	userprofile.gender = count % 3
	userprofile.mobile = cid + "000000"
	userprofile.institute = Institute.objects.get(institute_name = sample_institute_ids[0])
	userprofile.address = "IIT Bombay"
	userprofile.dob = datetime.now()
	userprofile.status = STATUS_APPROVED
	userprofile.save()
	userprofile.programs.add((count % 6)+1)
	studentprofile = StudentProfile()
	studentprofile.user = userprofile
	studentprofile.boe = BoardOfEducation.objects.get(boe_id = (count % 54)+1)
	studentprofile.roll_number = "12345"
	studentprofile.standard = Standard.objects.get(standard_id = (count % 5)+1)
	studentprofile.save()
	count += 1

for cid in sample_teacher_ids:
	np.random.shuffle(sample_institute_ids)
	user = User(username = cid)
	user.set_password(cid+cid)
	user.first_name = "CUSTOMER-" + cid[0] + cid[4]
	user.last_name = "teacher"
	user.email = "CUSTOMER-" + cid[0] + cid[4] + "@gmail.com"
	user.save()
	userprofile = UserProfile()
	userprofile.user = user
	userprofile.role = ROLE_TEACHER
	userprofile.gender = count % 3
	userprofile.mobile = cid + "000000"
	userprofile.institute = Institute.objects.get(institute_name = sample_institute_ids[0])
	userprofile.address = "IIT Bombay"
	userprofile.dob = datetime.now()
	userprofile.status = STATUS_APPROVED
	userprofile.save()
	userprofile.programs.add((count % 6)+1)
	teacherprofile = TeacherProfile()
	teacherprofile.user = userprofile
	teacherprofile.experience = "2 years"
	teacherprofile.save()
	count += 1

for cid in sample_insti_admin_ids:
	np.random.shuffle(sample_institute_ids)
	user = User(username = cid)
	user.set_password(cid+cid)
	user.first_name = "CUSTOMER-" + cid[0] + cid[4]
	user.last_name = "Insti_Admin"
	user.email = "CUSTOMER-" + cid[0] + cid[4] + "@gmail.com"
	user.save()
	userprofile = UserProfile()
	userprofile.user = user
	userprofile.role = ROLE_INSTITUTE_ADMIN
	userprofile.gender = count % 3
	userprofile.mobile = cid + "000000"
	userprofile.institute = Institute.objects.get(institute_name = sample_institute_ids[0])
	userprofile.address = "IIT Bombay"
	userprofile.dob = datetime.now()
	userprofile.status = STATUS_APPROVED
	userprofile.save()
	userprofile.programs.add((count % 6)+1)
	instituteAdmin = InstituteAdmin()
	instituteAdmin.user = userprofile
	instituteAdmin.save()
	instituteAdmin.institutes.add((count%7)+1, ((count+2)%7)+1)
	count += 1


# create chapters

sample_chapter_maths = ['limits', 'differentiation', 'continuity', 'coordinate geometry', 'integration']
sample_chapter_physics = ['electricity', 'magnetism', 'light', 'Force', 'units and measurement']
sample_chapter_chemistry = ['acids and bases', 'stochiometry', 'organic', 'inorganic', 'periodic elements']
sample_chapter_botany = ['The Living World', 'Plant Kingdom', 'Anatomy of Flowering Plants', 'Transport in Plants', 'Respiration in Plants']
sample_chapter_zoology = ['Biological Classification', 'Animal Kingdom', 'BioMolecules', 'Reproduction', 'Structural Organisation in Animals']
sample_chapter_GK = ['Sports', 'Politics', 'Economics', 'Environment', 'Railways']
subjects = ['1', '2', '3', '4', '5', '6']

for cid in subjects:
	temp = sample_chapter_maths
	if cid == '1':
		temp = sample_chapter_maths
	if cid == '2':
		temp = sample_chapter_physics
	if cid == '3':
		temp = sample_chapter_chemistry
	if cid == '4':
		temp = sample_chapter_botany
	if cid == '5':
		temp = sample_chapter_zoology
	if cid == '6':
		temp = sample_chapter_GK
	for i in range(5):
		chapter = Chapter()
		chapter.chapter_name = temp[i]
		chapter.subject = Subject.objects.get(subject_id = int(cid))
		chapter.save()


# create papers

PM = ['0', '1']
Paper_name = ['DPP1', 'DPP2', 'Exam1', 'Exam2', 'Exam3', 'Exam4']
count = 0
for name in Paper_name:
	paper = Paper()
	paper.paper_name = name
	paper.program = Program.objects.get(program_id = (count % 6) + 1)
	paper.paper_type = PaperType.objects.get(type_id = (count % 7) + 1)
	paper.teacher_id = TeacherProfile.objects.get(user__user__username = sample_teacher_ids[count % 5])
	paper.start_time = datetime.now()
	paper.end_time = datetime.now() + timedelta(days=7)
	paper.duration = 200
	paper.partial_marking = PM[count % 2]
	paper.save()
	paper.institutes.add((count%7)+1, ((count+1)%7)+1, ((count+2)%7)+1, ((count+3)%7)+1)
	paper.standards.add((count%5)+1, ((count+1)%5)+1)
	count = count + 1


# create question

Q_type = ['0', '1', '2', '3']
complexity = ['0', '1', '2', '3', '4']
sample_question = ['if A=90 deg , then sinA= ?', 'if A=90 deg , then cosA= ?', 'if A=90 deg , then tanA= ?', 'if A=90 deg , then cotA= ?', 'if A=90 deg , then secA= ?']
sample_solution = [0,1,2,3,4]
count = 1

for i in sample_question:
	for j in range(6):
		temp = sample_chapter_maths
		if j == '1':
			temp = sample_chapter_physics
		elif j == '2':
			temp = sample_chapter_chemistry
		elif j == '3':
			temp = sample_chapter_botany
		elif j == '4':
			temp = sample_chapter_zoology
		elif j == '5':
			temp = sample_chapter_GK
		question = Question()
		question.chapter = Chapter.objects.get(chapter_name = temp[count % 5])
		question.question_type = Q_type[count % 4]
		question.question = sample_question[count % 5]
		question.solution = sample_solution[count % 4]
		question.complexity = complexity[count % 5]
		question.teacher = TeacherProfile.objects.get(user__user__username = sample_teacher_ids[count % 5])
		question.marks_positive = 4
		question.marks_negative = -1
		if question.question_type == '3':
			question.int_answer = sample_solution[count % 5]
		elif question.question_type == '0':
			question.options =  [["A", "0", "0"], ["B", "1", "1"], ["C", "1", "2"], ["D", "0", "3"]]
		else:
			question.options =  [["A", "0", "0"], ["B", "0", "1"], ["C", "1", "2"], ["D", "0", "3"]]
		question.save()
		count = count + 1
		# mapping = Mapping()
		# mapping.paper = Paper.objects.get(paper_name = Paper_name[count % 5])
		# mapping.question = question
		# mapping.save()


# create attempt

count = 0
for i in range(1,31):
	attempt = Attempt()
	attempt.user = User.objects.get(username = sample_student_ids[count % 5])
	attempt.paper = Paper.objects.get(paper_id = (count%6)+1)
	attempt.status = count % 3
	attempt.start_time = datetime.now()
	attempt.end_time = datetime.now() + timedelta(minutes=3)
	attempt.save()
	count += 1


# create answer

count = 0
for i in range(1,31):
	question = Question.objects.get(question_id = (count%30)+1 )
	attempt = Attempt.objects.get(attempt_id = (count%30)+1)

	answer = None
	if Answer.objects.filter(question = question, attempt = attempt).exists():
		answer = Answer.objects.get(question = question, attempt = attempt)
	else:
		answer = Answer(question = question, attempt = attempt)

	if question.question_type == '3':
		answer.int_answer = sample_solution[count % 5]
	elif question.question_type == '0':
		answer.answer_array = ['C']
	else:
		answer.answer_array = ['C']
	answer.time_taken += int(count)
	answer.status = count % 3
	answer.marks_obtained = evaluate_answer(attempt.paper, question, answer)
	answer.save()
	count = count + 1