from django.shortcuts import render
from django.views.generic import RedirectView, DetailView, ListView, CreateView, UpdateView, DeleteView, TemplateView
from dashboard.models import *
# Create your views here.

class Questions(ListView):
	model = Question

	def get_queryset(self):
		return Question.objects.filter(cource=request.user.cource)

class LeadingQuestions(ListView):

	def get_queryset(self):
		return LeadingQuestion.objects.filter(course=self.request.user.course)


	def post(self, request, *args, **kwargs):
		if(request.POST.get('question')):
			p = LeadingQuestion.objects.filter(id=request.POST.get('question'))
			request.user.confidence.add(p)
			return JsonResponse({'result':True})
		return JsonResponse({'result':True})	

