from django.shortcuts import render
from django.views.generic import RedirectView, DetailView, ListView, CreateView, UpdateView, DeleteView
from dashboard.models import *
# Create your views here.

class Home(ListView):
	model = Question