from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser, UserManager
from ckeditor.fields import RichTextField
# User =  get_user_model()
from django.urls import reverse


class User(AbstractUser):
    confidence = models.ManyToManyField('dashboard.LeadingQuestion', blank=True)
    profile_visibility = models.BooleanField(default=True)
    sem = models.CharField(max_length=3, choices=[
        ('S2', 'B Tech S2'), 
        ('S4', 'B Tech S4'), 
        ('S6', 'B Tech S6'), 
        ('S8', 'B Tech S8'), 
        ('M2', 'M Tech S2'), 
        ('M4', 'M Tech S4'), 
    ], null=True, blank=True)
    batch = models.CharField(max_length=30, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    course = models.ForeignKey('dashboard.Course', on_delete=models.SET_NULL, null=True, blank=True)
    next_lesson = models.ForeignKey('dashboard.Lesson', on_delete=models.SET_NULL, null=True, blank=True)
    objects = UserManager()

    def __str__(self):
        return '{}, {}'.format(self.get_full_name(), self.sem)


class Course(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class Day(models.Model):
    name = models.IntegerField()

    def __str__(self):
        return 'Day {}'.format(self.name)


class Lesson(models.Model):
    order_number = models.PositiveSmallIntegerField(default=1, blank=True)
    title = models.CharField(max_length=120)
    explanation = RichTextField()
    course = models.ForeignKey('dashboard.Course', on_delete=models.CASCADE)
    day = models.ForeignKey('dashboard.Day', on_delete=models.CASCADE)
    completed = models.ManyToManyField('dashboard.User', blank=True)

    class Meta:
        ordering = ('order_number', 'id')

    def next(self):
        return Lesson.objects.filter(course=self.course, order_number__gt=self.order_number).first()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.order_number = (Lesson.objects.filter(course=self.course).aggregate(max=models.Max('order_number'))['max'] or 0) + 1
        return super().save(*args, **kwargs)

    def __str__(self):
        return "{}. {}".format(self.order_number, self.title)


class Question(models.Model):
    name = models.CharField(max_length=600)
    description = RichTextField()
    explanation = RichTextField(null=True, blank=True)
    logic = RichTextField(null=True, blank=True)
    hint = RichTextField(null=True, blank=True)
    answer = RichTextField(null=True, blank=True)
    lesson = models.ForeignKey('dashboard.Lesson', on_delete=models.CASCADE, null=True, blank=True)
    hint_viewed = models.ManyToManyField('dashboard.User', blank=True)

    def __str__(self):
        return self.name

    def get_url(self, user):
        sol = self.solution_set.filter(user=user).last()
        if sol:
            return reverse('solution-update', kwargs={'pk':sol.pk, 'question': self.question, 'day':user.next_task })  
        else:
            return reverse('solution', kwargs={'question': self.question, 'day':user.next_task })

    class Meta:
        ordering = ('id', )



class Reference(models.Model):
    link = models.URLField()
    description = models.TextField()
    lesson = models.ForeignKey('dashboard.Lesson', on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.lesson_id, self.link)


class Solution(models.Model):
    program = RichTextField(help_text="Write your program here.")
    question = models.ForeignKey('dashboard.Question', on_delete=models.CASCADE)
    user = models.ForeignKey('dashboard.User', on_delete=models.CASCADE)
    suggestions = RichTextField(null=True, blank=True)


class Score(models.Model):
    """ 
    
    Positive points is achievements, negative points are punishments! 
    Algorithm: 
        Everyone will get a free 100 points on initial.
        each logic unlock, 5 points will be reduced.

        1st lesson program will have 25 points. 
        each lesson above will have 25 + day_number * 10 + lesson order_number points


    """
    user = models.ForeignKey('dashboard.User', on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    remarks = models.CharField(max_length=100)

    def __str__(self):
        return '{}, {}'.format(self.user, self.score)


class LeadingQuestion(models.Model):
    title = models.CharField(max_length=300, default="", null=True)
    question = RichTextField()
    course = models.ForeignKey('dashboard.Course', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title






