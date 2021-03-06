from django.contrib.auth import views
from django.urls import include, path  # For django versions from 2.0 and up
from dashboard.views import *
from django.contrib.auth.decorators import login_required as __

lesson_view = __(LessonView.as_view())
leading_questions = __(LeadingQuestions.as_view())
# solution = __(SubmitSolution.as_view())
question = __(QuestionView.as_view())
faq = __(FAQListView.as_view())
faq_detail = __(FAQDetailView.as_view())
faq_form = __(CreateView.as_view(model=WantedFAQ, form_class=WantedFAQForm, success_url=reverse_lazy('faq-list')))
identifiers = __(IdentifierListView.as_view(model=Identifier))

namespace = "dashboard"

urlpatterns = [
	path('', TemplateView.as_view(template_name='dashboard/index.html'), name='home'),
	path('self-assessment/', leading_questions, name='self-assessment'),
	path('lesson-<int:pk>/', lesson_view, name='daily_task'),
	path('question-<int:pk>/', question , name='question'),
	# path('question-<int:question>/solution/', solution, name='solution'),
	path('faq/', faq, name='faq-list'),
	path('faq/<slug:slug>/', faq_detail, name='faq-detail'),
	path('responses/', include('django_comments.urls')),
	path('faq-wanted/', faq_form, name='faq-wanted'),
	path('needs-improvement/', needs_improvement, name='needs-improvement-api'),
	path('identifiers/', identifiers, name='identifiers'),
	path('clip-it/', clip_it, name='clip-it-api'),
	path('compiler/python/', check_python_api, name='compiler-python-api'),
	path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
	path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]
