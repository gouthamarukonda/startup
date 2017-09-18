from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^create/$', views.program_create),
	url(r'^fetchprograms/$', views.get_all_programs),
]
