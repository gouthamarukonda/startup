from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^create/$', views.paper_create),
	url(r'^createmapping/$', views.mapping_create),
]
