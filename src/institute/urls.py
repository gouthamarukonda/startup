from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^register/$', views.institute_register),
	url(r'^registeradmin/$', views.register_admin),
]
