from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser, UserManager

# User =  get_user_model()

 
class User(AbstractUser):
    confidence = models.ManyToManyField('dashboard.LeadingQuestion')
    hint_viewed = models.ManyToManyField('dashboard.Question')
    profile_visibility = models.BooleanField(default=True)
    sem = models.CharField(max_length=3, choices=[
        ('S2', 'B Tech S2'), 
        ('S4', 'B Tech S4'), 
        ('S6', 'B Tech S6'), 
        ('S8', 'B Tech S8'), 
        ('M2', 'M Tech S2'), 
        ('M4', 'M Tech S4'), 
    ], null=True)

    objects = UserManager()


class Score(models.Model):
    """ Positive points is achievements, negative points are punishments! """
    user = models.ForeignKey('dashboard.User', on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    remarks = models.CharField(max_length=50)

class Course(models.Model):
    name = models.CharField(max_length=30)


class Day(models.Model):
    name = models.IntegerField()


class Question(models.Model):
    name = models.CharField(max_length=30)
    cource = models.ForeignKey('dashboard.Course', on_delete=models.CASCADE)
    day = models.ForeignKey('dashboard.Day', on_delete=models.CASCADE)
    level = models.PositiveSmallIntegerField(choices=[(1, 'new'), (2, 'intermediate'), (3, 'advanced')], default=1)
    description =  models.TextField()
    explanation =  models.TextField()
    logic =  models.TextField()
    hint =  models.TextField()


class Reference(models.Model):
    link = models.URLField()
    question = models.ForeignKey('dashboard.Question', on_delete=models.CASCADE)


class Solution(models.Model):
    program =  models.TextField()
    question = models.ForeignKey('dashboard.Question', on_delete=models.CASCADE)
    user = models.ForeignKey('dashboard.User', on_delete=models.CASCADE)
    suggestions = models.TextField()


class Achievement(models.Model):
    program =  models.TextField()
    question = models.ForeignKey('dashboard.Question', on_delete=models.CASCADE)


class LeadingQuestion(models.Model):
    question = models.TextField()







