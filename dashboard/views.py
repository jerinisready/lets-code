from django.shortcuts import render
from django.views.generic import RedirectView, DetailView, ListView, CreateView, UpdateView, DeleteView, TemplateView
from dashboard.models import *
# Create your views here.

class Questions(ListView):
	model = Question


class LeadingQuestions(ListView):
	model = LeadingQuestion
