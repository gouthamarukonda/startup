from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^create/$', views.paper_create),
	url(r'^add_question/$', views.add_question),
	url(r'^papertype/create/$', views.paper_type_create),
]
