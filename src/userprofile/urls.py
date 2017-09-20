from django.conf.urls import url, include
from . import views
from . import views_admin

admin_patterns = [
	url(r'^view-programs/$', views_admin.template_view_all_programs),
	url(r'^view-subjects/$', views_admin.template_view_all_subjects),
	url(r'^view-institutes/$', views_admin.template_view_all_institutes),
	url(r'^view-institute-admins/$', views_admin.template_view_all_institute_admins),
	url(r'^edit-program/(?P<id>\d+)/$', views_admin.template_edit_program),
	url(r'^edit-subject/(?P<id>\d+)/$', views_admin.template_edit_subject),
	url(r'^edit-institute/(?P<id>\d+)/$', views_admin.template_edit_institute),
	url(r'^edit-institute-admin/(?P<id>\d+)/$', views_admin.template_edit_institute_admin),
	url(r'^delete-program/(?P<id>\d+)/$', views_admin.template_delete_program),
	url(r'^delete-subject/(?P<id>\d+)/$', views_admin.template_delete_subject),
]

urlpatterns = [
	url(r'^disapprove/$', views.user_disapprove),
	url(r'^login/$', views.user_login),
	url(r'^home/$', views.get_user_home_page),
	url(r'^usernameverification/$', views.username_verification),
	url(r'^emailverification/$', views.email_verification),
	url(r'^validatepassword/$', views.password_validation),
	url(r'^admin/', include(admin_patterns)),
]
