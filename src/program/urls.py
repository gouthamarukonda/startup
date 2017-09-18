from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^create/$', views.program_create),
	url(r'^getallprograms/$', views.get_all_programs),
]
