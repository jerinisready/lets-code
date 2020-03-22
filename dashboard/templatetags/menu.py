from django import template
from django.urls import reverse_lazy, reverse
from django.utils.safestring import mark_safe
from dashboard.models import Day

register = template.Library()

"""
                <li class="app-sidebar__heading">Dashboard</li>
                <li><a {{ "dashboard:index"|menu_anchor:request }}><i class="metismenu-icon pe-7s-rocket"></i>Home</a></li>
                <li class="app-sidebar__heading">Invoices</li>

                    <li><a {{ "dashboard:requests|status=new"|menu_anchor:request }}><i class="metismenu-icon pe-7s-rocket"></i> New Requests </a></li>
                    <li class="{{ request|if_invoice:"mm-active" }}">
                        <a {{ request|if_invoice:'aria-expanded="true"' }} href="#"><i class="metismenu-icon pe-7s-diamond"></i>  Requests <i class="metismenu-state-icon pe-7s-angle-down caret-left"></i></a>
                        <ul class="mm-collapse {{ request|if_invoice:'mm-show' }}">
                            <li><a {{ "dashboard:requests|status=new"|menu_anchor:request }}><i class="metismenu-icon"></i> New Requests </a></li>
                            <li><a {{ "dashboard:requests|status=approved"|menu_anchor:request }}><i class="metismenu-icon"></i> Approved Requests </a></li>
                            <li><a {{ "dashboard:requests|status=rejected"|menu_anchor:request }}><i class="metismenu-icon"></i> Rejected Requests </a></li>
                        </ul>
                    </li>
"""



@register.simple_tag
def params(field_name, value=None, urlencode=None):
    if value:
        url = '?{}={}'.format(field_name, value)
    else:
        url = '?'
    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url, encoded_querystring)
    return url.rstrip('&')



@register.simple_tag
def query_filter(qs, **kwargs):
    """ template tag which allows queryset filtering. Usage:
          {% query books author=author as mybooks %}
          {% for book in mybooks %}
            ...
          {% endfor %}
    """
    return qs.filter(**kwargs)

@register.filter(is_safe=True)
def menu_anchor(_name: str, request):
    if not _name:
        return "''"
    name, param_strings = _name.split('|') if '|' in _name else (_name, None)
    constructed_url = request.resolver_match.view_name
    if param_strings:
        constructed_url += '|pk=' + str(request.resolver_match.kwargs.get('pk'))
    class_if_active = 'mm-active' if _name == constructed_url else ''
    param_strings = {
        k: v for k, v in [_str.split('=') for _str in param_strings.split('&') if _str] if k and v
    } if param_strings else {}
    url = reverse(name, kwargs=param_strings)
    html = f'href="{url}" class="{class_if_active}"'
    return mark_safe(html)


@register.filter(is_safe=True)
def if_day(request, text: str):
    out = request.resolver_match.view_name
    return text if out in ['daily_task', ] else ''

@register.simple_tag
def day_list(request):
    out = []
    days = Day.objects.all().order_by('name').prefetch_related('lesson_set')
    for day in days:
        out.append({'day': day, 
            'menu_anchor_filter': "daily_task|pk={}".format(day.pk),
            'lessons': [ {'menu_anchor_filter':"daily_task|pk={}".format(l.pk), 'lesson': l } for l in day.lesson_set.all() if l.course_id == request.user.course_id]  # reduces db hit. and not much in number         
            })
    return out

@register.simple_tag
def exec_function(func, *args, **kwargs):
    return func(*args, **kwargs)
    
