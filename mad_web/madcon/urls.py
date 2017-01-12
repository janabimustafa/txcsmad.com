# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    # URL pattern for the Events
    url(
        regex=r'^register/$',
        view=login_required(views.MADconRegistrationView.as_view()),
        name='register'
    ),
    url(
        regex=r'^status/$',
        view=login_required(views.MADconRegistrationStatusView.as_view()),
        name='status'
    ),
    url(
        regex=r'^confirm/$',
        view=login_required(views.MADconConfirmAttendanceView.as_view()),
        name='confirm'
    ),
]
