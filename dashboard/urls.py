
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.urls import include, path  # For django versions from 2.0 and up
from dashboard.views import *
from django.contrib.auth.decorators import login_required as __

lesson_view = __(LessonView.as_view())
leading_questions = __(LeadingQuestions.as_view())
solution = __(SubmitSolution.as_view())
question = __(QuestionView.as_view())


namespace = "dashboard"

urlpatterns = [
	path('', leading_questions, name='home'),
	path('lesson-<int:pk>/', lesson_view, name='daily_task'),
	path('question-<int:pk>/', question , name='question'),
	path('question-<int:question>/solution/', solution, name='solution'),

]