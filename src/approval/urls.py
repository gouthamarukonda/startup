from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^submitrequest/$', views.submit_approval_request),
	url(r'^updatestatus/$', views.update_status),
]
