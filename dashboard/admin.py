from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.

from dashboard.models import * 

create_panel = admin.site.register

create_panel(User, UserAdmin)

create_panel(Course)
create_panel(Day)
create_panel(Question)
create_panel(Reference)
create_panel(Solution)
create_panel(Achievement)
create_panel(LeadingQuestion)
create_panel(Score)
