
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.urls import include, path  # For django versions from 2.0 and up
from dashboard.views import *
from django.contrib.auth.decorators import login_required as __

daily_task = __(DailyTask.as_view())
leading_questions = __(LeadingQuestions.as_view())
solution = __(SubmitSolution.as_view())


namespace = "dashboard"

urlpatterns = [
	path('', leading_questions, name='home'),
	path('day-<int:pk>/', daily_task, name='daily_task'),
	path('day-<int:day>/question-<int:question>/solution/', solution, name='solution'),

]