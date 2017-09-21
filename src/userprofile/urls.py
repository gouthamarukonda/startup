from django.conf.urls import include, url

from . import views
from . import views_admin

admin_urlpatterns = [
	url(r'^view-programs/$', views_admin.template_view_all_programs),
	url(r'^view-subjects/$', views_admin.template_view_all_subjects),
	url(r'^view-institutes/$', views_admin.template_view_all_institutes),
	url(r'^view-institute-admins/$', views_admin.template_view_all_institute_admins),
	url(r'^edit-program/(?P<id>\d+)/$', views_admin.template_edit_program),
	url(r'^edit-subject/(?P<id>\d+)/$', views_admin.template_edit_subject),
	url(r'^edit-institute/(?P<id>\d+)/$', views_admin.template_edit_institute),
	url(r'^edit-institute-admin/(?P<id>\d+)/$', views_admin.template_edit_institute_admin),
	url(r'^update-program/$', views_admin.template_update_program),
	url(r'^update-subject/$', views_admin.template_update_subject),
	url(r'^update-institute/$', views_admin.template_update_institute),
	url(r'^update-institute-admin/$', views_admin.template_update_institute_admin),
	url(r'^delete-program/$', views_admin.template_delete_program),
	url(r'^delete-subject/$', views_admin.template_delete_subject),
	url(r'^delete-institute/$', views_admin.template_delete_institute),
	url(r'^delete-institute-admin/$', views_admin.template_delete_institute_admin),
]

urlpatterns = [
	url(r'^admin/', include(admin_urlpatterns)),
	url(r'^disapprove/$', views.user_disapprove),
	url(r'^login/$', views.user_login),
	url(r'^home/$', views.get_user_home_page),
	url(r'^usernameverification/$', views.username_verification),
	url(r'^emailverification/$', views.email_verification),
	url(r'^validatepassword/$', views.password_validation),
	url(r'^updateprofilepicture/$', views.update_profile_picture),
	url(r'^getprofilepicture/$', views.get_profile_picture),
]
