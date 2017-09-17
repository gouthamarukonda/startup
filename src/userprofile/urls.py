from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^approve/$', views.user_approve),
	url(r'^disapprove/$', views.user_disapprove),
	url(r'^login/$', views.user_login),
	url(r'^home/$', views.get_user_home_page),

]
