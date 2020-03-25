import datetime

from django.core.cache import cache
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.utils import timezone
from django_extensions.db.fields import AutoSlugField


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

    def last_seen(self):
        return cache.get('seen_%s' % self.pk)

    def online(self):
        if self.last_seen():
            now = timezone.now()
            if now <= self.last_seen() + datetime.timedelta(
                         seconds=settings.USER_ONLINE_TIMEOUT):
                return True
        return False


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
            return reverse('solution-update', kwargs={'pk': sol.pk, 'question': self.question, 'day': user.next_task })
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
    program = models.TextField(help_text="Write your program here.")
    question = models.ForeignKey('dashboard.Question', on_delete=models.CASCADE)
    user = models.ForeignKey('dashboard.User', on_delete=models.CASCADE)
    suggestions = RichTextField(null=True, blank=True)

    def __str__(self):
        return '{}, {}'.format(self.user, self.program)


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


class FAQ(models.Model):
    title = models.CharField(max_length=300, default="", null=True)
    slug = AutoSlugField(max_length=300, populate_from=("title", ), overwrite=True, editable=True, unique=True)
    explanation = RichTextField(null=True, blank=True)
    clip_it = models.ManyToManyField('dashboard.User', blank=True, related_name='clipped_items')
    needs_improvement = models.ManyToManyField('dashboard.User', blank=True, related_name='voted_needs_improvement')
    related_lessons = models.ManyToManyField('dashboard.Lesson', blank=True)

    def __str__(self):
        return self.title


class WantedFAQ(models.Model):
    title = models.TextField()
    user = models.ForeignKey('dashboard.User', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title


BUILTIN_CHOICES = [
    (0, 'KeyWord'),
    (1, 'Operator'),
    (2, 'Builtin Functions'),
]


class Identifier(models.Model):
    token_type = models.PositiveSmallIntegerField(choices=BUILTIN_CHOICES, default=0)
    name = models.CharField(max_length=40, unique=True)
    description = RichTextField()
    # code = RichTextField(null=True, blank=True)
    code = models.TextField(null=True, blank=True)
    supporting_versions = models.CharField(max_length=120, default='all', null=True, blank=True)
    slug = AutoSlugField(max_length=50, populate_from=('name', ), overwrite=True, editable=True, unique=True)

    @property
    def token(self):
        return ['KeyWord', 'Operator', 'Builtin Functions'][self.token_type]

    def __str__(self):
        return self.name




