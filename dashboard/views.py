from django.shortcuts import render

# Create your views here.

class Home(ListView):
	model = Question