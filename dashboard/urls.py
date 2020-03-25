from django.urls import include, path  # For django versions from 2.0 and up
from dashboard.views import *
from django.contrib.auth.decorators import login_required as __

lesson_view = __(LessonView.as_view())
leading_questions = __(LeadingQuestions.as_view())
solution = __(SubmitSolution.as_view())
question = __(QuestionView.as_view())
faq = __(FAQListView.as_view())
faq_detail = __(FAQDetailView.as_view())
faq_form = __(CreateView.as_view(model=WantedFAQ, form_class=WantedFAQForm, success_url=reverse_lazy('faq-list')))


def needs_improvement(request):
	post = request.DATA.get
	if request.user.is_authenticated and request.method == 'POST' and post('status') and post('faq'):
		_faq = FAQ.objects.filter(pk=post('faq')).last()
		if _faq:
			if post('status') == 'remove':
				_faq.needs_improvement.remove(request.user)
			if post('status') == 'add':
				_faq.needs_improvement.add(request.user)
			return JsonResponse({'response': 'updated'})
	return JsonResponse({'response': None}, status=400)


def clip_it(request):
	post = request.DATA.get
	if request.user.is_authenticated and request.method == 'POST' and post('status') and post('faq'):
		_faq = FAQ.objects.filter(pk=post('faq')).last()
		if _faq:
			if post('status') == 'remove':
				_faq.clip_it.remove(request.user)
			if post('status') == 'add':
				_faq.needs_improvement.add(request.user)
			return JsonResponse({'response': 'updated'})
	return JsonResponse({'response': None}, status=400)


namespace = "dashboard"

urlpatterns = [
	path('', TemplateView.as_view(template_name='dashboard/index.html'), name='home'),
	path('self-assessment/', leading_questions, name='self-assessment'),
	path('lesson-<int:pk>/', lesson_view, name='daily_task'),
	path('question-<int:pk>/', question , name='question'),
	path('question-<int:question>/solution/', solution, name='solution'),
	path('faq/', faq, name='faq-list'),
	path('faq/<slug:slug>/', faq_detail, name='faq-detail'),
	path('responses/', include('django_comments.urls')),
	path('faq-wanted/', faq_form, name='faq-wanted'),

	path('needs-improvement/', needs_improvement, name='needs-improvement-api'),
	path('clip-it/', clip_it, name='clip-it-api'),

]
