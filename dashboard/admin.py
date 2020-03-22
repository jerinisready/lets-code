from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.

from dashboard.models import * 

create_panel = admin.site.register

_ = lambda x:x

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password', 'course')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'sem', 'profile_visibility', 'batch', 'remarks')}),
        (_('Internal Use'), {'fields': ('confidence', 'hint_viewed', )}),
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
    list_display = ('username', 'get_full_name', 'sem', 'batch', 'email', 'course')
    list_filter = ('sem', 'batch', 'is_active', 'profile_visibility', 'course')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'sem', 'batch')



create_panel(User, CustomUserAdmin)

create_panel(Course)
create_panel(Day)
create_panel(Question)
create_panel(Reference)
create_panel(Solution)
create_panel(Achievement)
create_panel(LeadingQuestion)
create_panel(Score)
