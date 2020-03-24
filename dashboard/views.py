from django.shortcuts import render
from django.views.generic import RedirectView, DetailView, ListView, CreateView, UpdateView, DeleteView, TemplateView
from dashboard.models import *
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import *
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, QueryDict

# Create your views here.


class LeadingQuestions(ListView):

    def get_queryset(self):
        if self.request.user.course:
            return LeadingQuestion.objects.filter(course=self.request.user.course)\
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


class SubmitSolution(UpdateView):
    model = Solution
    question_object = None
    fields = ('program', )

    def get_question_object(self):
        pk = self.kwargs.get('question')
        if self.question_object is None:
            self.question_object = get_object_or_404(Question.objects.all(), **{'pk':pk})
        return self.question_object

    def get_success_url(self):
        from django.urls import reverse_lazy
        messages.success(self.request, "Solution Submitted!")
        return reverse_lazy('daily_task', self.request.user.next_task)

    def get_context_data(self, **kwargs):
        return super().get_context_data(question=self.get_question_object(), **kwargs)

    def get_object(self, queryset=None):
        try:
            return self.model.objects.filter(user=self.request.user, question=self.get_question_object()).first()
        except Exception as e:
            return None 

    def form_valid(self, form):
        form.cleaned_data['user'] = self.request.user
        form.cleaned_data['question'] = self.get_question_object()
        form.save(commit=False)
        form.instance.user = self.request.user
        form.instance.question = self.get_question_object()
        form.instance.save()
        return HttpResponseRedirect(f'/board/question-{self.kwargs.get("question")}/?give_solution')


class QuestionView(DetailView):
    model = Question
