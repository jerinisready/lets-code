
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.urls import include, path  # For django versions from 2.0 and up
from dashboard.views import *
from django.contrib.auth.decorators import login_required as __

questions = __(Questions.as_view())
leading_questions = __(LeadingQuestions.as_view())



namespace = "dashboard"

urlpatterns = [
	path('', leading_questions, name='home'),
	path('questions/', questions, name='questions')
]