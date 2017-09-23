from django.contrib import admin

from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'role', 'gender', 'dob', 'mobile', 'address', 'profile_picture', 'institute', 'PROGRAMS', 'status')
	fields = ('user' , 'role', 'gender', 'dob', 'mobile', 'address', 'profile_picture', 'institute', 'programs', 'status')

admin.site.register(UserProfile, UserProfileAdmin)
