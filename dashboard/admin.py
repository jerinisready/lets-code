from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.

from dashboard.models import * 

create_panel = admin.site.register

_ = lambda x:x

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password', 'course', )}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'sem',
                                         'profile_visibility', 'batch', 'remarks')}),
        (_('Internal Use'), {'fields': ('confidence', )}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', ),
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'sem', 'first_name', 'last_name', 'batch'),
        }),
    )
    list_display = ('username', 'get_full_name', 'sem', 'batch', 'email', 'course', )
    list_filter = ('sem', 'batch', 'is_active', 'profile_visibility', 'course', )
    search_fields = ('username', 'first_name', 'last_name', 'email', 'sem', 'batch')


class CustomLessonAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'day',  'course',)
    list_filter = ('day', 'course', )


class CustomQuestionAdmin(admin.ModelAdmin):
    list_filter = ('lesson', 'lesson__course', 'lesson__day' )


class SolutionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'question', )
    list_filter = ('user',  'question__lesson', )


create_panel(User, CustomUserAdmin)

create_panel(Course)
create_panel(Day)
create_panel(Lesson, CustomLessonAdmin)
create_panel(Question, CustomQuestionAdmin)
create_panel(Reference)
create_panel(Solution, SolutionAdmin)
create_panel(LeadingQuestion)
create_panel(Score)



from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import gettext_lazy as _

# Define a new FlatPageAdmin
class FlatPageAdmin(FlatPageAdmin):
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites')}),
        (_('Advanced options'), {
            'classes': ('collapse',),
            'fields': (
                'enable_comments',
                'registration_required',
                'template_name',
            ),
        }),
    )

# Re-register FlatPageAdmin
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)