from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^create/$', views.question_create),
	url(r'^delete/$', views.question_delete),
	url(r'^submitanswer/$', views.submit_answer),
]
