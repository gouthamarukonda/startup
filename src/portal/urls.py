"""portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from userprofile import views as userprofile_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', userprofile_views.get_login_page),
    url(r'^user/', include('userprofile.urls')),
    url(r'^student/', include('student.urls')),
    url(r'^teacher/', include('teacher.urls')),
    url(r'^institute/', include('institute.urls')),
    url(r'^paper/', include('paper.urls')),
    url(r'^chapter/', include('chapter.urls')),
    url(r'^question/', include('question.urls')),
    url(r'^answer/', include('answer.urls')),
    url(r'^approval/', include('approval.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
