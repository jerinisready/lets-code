import json

from django import forms
from django.forms import ModelForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import RedirectView, DetailView, ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.views.generic.edit import FormMixin

from dashboard.models import *
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import *
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, QueryDict

# Create your views here.
from utils.compilers import run_python


class LeadingQuestions(ListView):

    def get_queryset(self):
        if self.request.user.course:
            return LeadingQuestion.objects.filter(course=self.request.user.course) \
                .annotate(is_confident=Exists(self.request.user.confidence.filter(id=OuterRef('pk'))))
        return LeadingQuestion.objects.none()

    def post(self, request, *args, **kwargs):
        if request.POST.get('question'):
            p = LeadingQuestion.objects.filter(id=request.POST.get('question')).last()
            if p:
                request.user.confidence.add(p)
                messages.success(self.request, "Assessment Marked")
        return self.get(request, *args, **kwargs)

# ======================================================================================


class LessonView(DetailView):

    object = None

    def get_object(self, queryset=None):
        if not self.object:
            self.object = super().get_object(queryset)
        return self.object

    def get_queryset(self):
        return Lesson.objects.filter(course=self.request.user.course).prefetch_related('question_set', 'reference_set').select_related('course', 'day', )

    def get_context_data(self, **kwargs):
        if self.request.user.course:
            qn_list =  self.get_object().question_set.all()
        return super(LessonView, self).get_context_data(questions=qn_list, **kwargs)

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        self.request.user.next_lesson = obj.next()
        self.request.user.save()
        messages.success(self.request, "Congrats! Welcome to Next Lesson ")
        return self.get(request, *args, **kwargs)


# class SubmitSolution(UpdateView):
#     model = Solution
#     question_object = None
#     fields = ('program', )
#
#     def get_question_object(self):
#         pk = self.kwargs.get('question')
#         if self.question_object is None:
#             self.question_object = get_object_or_404(Question.objects.all(), **{'pk':pk})
#         return self.question_object
#
#     def get_success_url(self):
#         from django.urls import reverse_lazy
#         messages.success(self.request, "Solution Submitted!")
#         return reverse_lazy('daily_task', self.request.user.next_task)
#
#     def get_context_data(self, **kwargs):
#         return super().get_context_data(question=self.get_question_object(), **kwargs)
#
#     def get_object(self, queryset=None):
#         try:
#             return self.model.objects.filter(user=self.request.user, question=self.get_question_object()).first()
#         except Exception as e:
#             return None
#
#     def form_valid(self, form):
#         form.cleaned_data['user'] = self.request.user
#         form.cleaned_data['question'] = self.get_question_object()
#         form.save(commit=False)
#         form.instance.user = self.request.user
#         form.instance.question = self.get_question_object()
#         form.instance.save()
#         return HttpResponseRedirect(f'/board/question-{self.kwargs.get("question")}/?give_solution')


class QuestionView(DetailView):
    model = Question
    solution = None

    def get_solution(self):
        if not self.solution:
            self.solution = Solution.objects.filter(question=self.kwargs['pk'], user=self.request.user).last() or Solution()
        return self.solution

    def get_context_data(self, **kwargs):
        kwargs = super(QuestionView, self).get_context_data(**kwargs)
        kwargs['solution'] = self.get_solution()
        return kwargs

    def post(self, request, *args, **kwargs):
        if self.request.POST.get('program'):
            solution = self.get_solution()
            solution.program = self.request.POST.get('program')
            if not solution.pk:
                solution.question = self.get_object()
                solution.user = self.request.user
            solution.save()
            messages.success(request, "Program Saved!")
        return self.get(request, *args, **kwargs)


class CreateWantedFAQView(CreateView):
    model = WantedFAQ


# ========================================================================


class WantedFAQForm(ModelForm):
    class Meta:
        model = WantedFAQ
        fields = ('title', )


class FAQDetailView(DetailView):

    def get_queryset(self):
        return FAQ.objects.all().annotate(
            upvoted=Exists(self.request.user.clipped_items.filter(id=OuterRef('pk'))),
            downvoted=Exists(self.request.user.voted_needs_improvement.filter(id=OuterRef('pk'))),
        )


class FAQListView(ListView):

    paginate_by = 30

    def get_queryset(self):
        return FAQ.objects.all().filter(course=self.request.user.course).annotate(
            upvoted=Exists(self.request.user.clipped_items.filter(id=OuterRef('pk'))),
            downvoted=Exists(self.request.user.voted_needs_improvement.filter(id=OuterRef('pk'))),
        )

    def get_context_data(self, *a, object_list=None, **kwargs):
        return super(FAQListView, self).get_context_data(*a,
                                                         faq_survey_submit_url=reverse_lazy('faq-wanted'),
                                                         faq_survey_form=WantedFAQForm,
                                                         **kwargs)


class IdentifierListView(ListView):

    def get_queryset(self):
        return Identifier.objects.all().filter(course=self.request.user.course)


@csrf_exempt
def check_python_api(request):
    out = None
    _type = None
    stat = 400
    data = json.loads(request.body)
    if request.method == 'POST' and data.get('program') and request.user.is_authenticated:
        program = data.get('program', '')
        sample_input = data.get('input', '')
        out, error = run_python(program, sample_input)
        stat = 200
    return JsonResponse({
        'out': out,
        'error': error,
        'authenticated': request.user.is_authenticated
    }, status=stat)


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

