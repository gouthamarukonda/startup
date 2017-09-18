from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^create/$', views.program_create),
	url(r'^fetchprograms/$', views.get_all_programs),
	url(r'^standard/create/$', views.standard_create),
	url(r'^fetchstandards/$', views.get_all_standards),
]
