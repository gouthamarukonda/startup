from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

from institute.models import Institute
from program.models import Program

ROLE_STUDENT = '0'
ROLE_TEACHER = '1'
ROLE_INSTITUTE_ADMIN = '2'

ROLE_CHOICES = (
	(ROLE_STUDENT, 'student'),
	(ROLE_TEACHER, 'teacher'),
	(ROLE_INSTITUTE_ADMIN, 'Institute Admin'),
)

GENDER_MALE = '0'
GENDER_FEMALE = '1'
GENDER_OTHER = '2'

GENDER_CHOICES = (
	(GENDER_MALE, "Male"),
	(GENDER_FEMALE, "Female"),
	(GENDER_OTHER, "Other")
)

STATUS_UNAPPROVED = '0'
STATUS_APPROVED = '1'

STATUS_CHOICES = (
	(STATUS_APPROVED, "Registration Approved"),
	(STATUS_UNAPPROVED, "Registration Not Approved"),
)

class UserProfile(models.Model):

	user = models.OneToOneField(User, db_column = 'user_id', primary_key = True, on_delete = models.CASCADE)
	role = models.CharField("Role", db_column = 'role', choices = ROLE_CHOICES, max_length = 1, default = ROLE_STUDENT)
	gender = models.CharField("Gender", db_column = 'gender', choices = GENDER_CHOICES, max_length = 1, default = GENDER_MALE)
	dob = models.DateTimeField("Date of Birth", db_column='dob', blank=True)
	mobile = models.CharField("Mobile Number", db_column = 'mobile', max_length = 15, blank = True)
	address = models.CharField("Address", max_length = 1000, blank = True)
	profile_picture = ProcessedImageField(upload_to = 'profilepictures',
										  processors = [ResizeToFill(360, 360, upscale = True)],
										  format = 'JPEG',
										  options = {'quality': 72},
										  null = True)
	institute = models.ForeignKey(Institute, db_column = 'institute', on_delete = models.CASCADE)
	programs = models.ManyToManyField(Program, db_column = 'programs')
	status = models.CharField("Registration Status", db_column = 'status', choices = STATUS_CHOICES, max_length = 1, default = STATUS_UNAPPROVED)

	class Meta:
		db_table = 'user_profile'

	def get_profile_picture_url(self):
		if self.profile_picture:
			return self.profile_picture.url
		else:
			return settings.DEFAULT_PROFILE_PICTURE_URL

	def __unicode__(self):
		return unicode(self.user)

	def PROGRAMS(self):
		return ", ".join([str(p.program_name) for p in self.programs.all()])
