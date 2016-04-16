# -*- coding: utf-8 -*-
# -*- date: 2016-04-13 22:32 -*-

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.admin_backup, name='admin_backup')
]
