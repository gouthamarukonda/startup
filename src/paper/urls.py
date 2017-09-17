from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^create/$', views.paper_create),
	url(r'^add_question/$', views.add_question),
]
