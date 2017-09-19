from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^register/$', views.student_register),
	url(r'^boe/create/$', views.boe_create),
	url(r'^fetchboards/$', views.get_all_boards),
]
