"""league URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from league_tracker import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^add_user/', views.create_user),
    url(r'^add_deck/', views.create_deck),
    url(r'^add_record/', views.create_record),
    url(r'^add_event/', views.create_event),
    url(r'^update_record/(?P<id>\d+)/$', views.update_record),
    url(r'^delete_record/(?P<id>\d+)/$', views.delete_record),
    url(r'^records/(?P<id>\d+)/$', views.records),
    url(r'^records/$', views.all_records),
    url(r'^statistics/$', views.statistics),
    url(r'^$', views.index),
]
