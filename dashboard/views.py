from django.shortcuts import render
from django.views.generic import RedirectView, DetailView, ListView, CreateView, UpdateView, DeleteView, TemplateView
from dashboard.models import *
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import *

# Create your views here.
class LeadingQuestions(ListView):

	def get_queryset(self):
		if self.request.user.course:
			return LeadingQuestion.objects.filter(course=self.request.user.course)\
			.annotate(is_confident=Exists(self.request.user.confidence.filter(id=OuterRef('pk'))))
		return LeadingQuestion.objects.none()	


	def post(self, request, *args, **kwargs):
		if(request.POST.get('question')):
			p = LeadingQuestion.objects.filter(id=request.POST.get('question')).last()
			if p:
				request.user.confidence.add(p)
		return self.get(request, *args, **kwargs)

# ======================================================================================


class DailyTask(DetailView):
	queryset = Day.objects.all().prefetch_related('question_set')

	def get_conext_data(self, **kwargs):
		if self.request.user.course:
			qn_list =  Question.objects.filter(course=self.request.user.course, day=self.object)
		return super(DailyTask, self).get_conext_data(questions=qn_list, **kwargs)

