from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser, UserManager

# User =  get_user_model()

 
class User(AbstractUser):
    confidence = models.ManyToManyField('dashboard.LeadingQuestion', blank=True)
    hint_viewed = models.ManyToManyField('dashboard.Question', blank=True)
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

    objects = UserManager()

    def __str__(self):
        return '{}, {}'.format(self.get_full_name(), self.sem)

class Score(models.Model):
    """ Positive points is achievements, negative points are punishments! """
    user = models.ForeignKey('dashboard.User', on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    remarks = models.CharField(max_length=100)

    def __str__(self):
        return '{}, {}'.format(self.user, score)

class Course(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name

class Day(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return 'Day {}'.format(self.name)

class Question(models.Model):
    name = models.CharField(max_length=600)
    cource = models.ForeignKey('dashboard.Course', on_delete=models.CASCADE)
    day = models.ForeignKey('dashboard.Day', on_delete=models.CASCADE)
    level = models.PositiveSmallIntegerField(choices=[(1, 'new'), (2, 'intermediate'), (3, 'advanced')], default=1)
    description =  models.TextField()
    explanation =  models.TextField(null=True, blank=True)
    logic =  models.TextField(null=True, blank=True)
    hint =  models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Reference(models.Model):
    link = models.URLField()
    question = models.ForeignKey('dashboard.Question', on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.question, self.link)


class Solution(models.Model):
    program =  models.TextField()
    question = models.ForeignKey('dashboard.Question', on_delete=models.CASCADE)
    user = models.ForeignKey('dashboard.User', on_delete=models.CASCADE)
    suggestions = models.TextField(null=True, blank=True)


class Achievement(models.Model):
    program =  models.TextField()
    question = models.ForeignKey('dashboard.Question', on_delete=models.CASCADE)


class LeadingQuestion(models.Model):
    question = models.TextField()
    course   = models.ForeignKey('dashboard.Course', on_delete=models.CASCADE, null=True, blank=True)






