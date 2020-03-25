import os

from django.conf import settings
from django.core.cache import cache
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

USER_ONLINE_TIMEOUT = getattr(settings, 'USER_ONLINE_TIMEOUT', 300)  # 5 minutes
ONLINE_MAX = getattr(settings, 'ONLINE_MAX', 50)


def get_online_now(self):
    return User.objects.filter(id__in=self.online_now_ids or [])


class OnlineNowMiddleware(MiddlewareMixin):
    """
    Maintains a list of users who have interacted with the website recently.
    Their user IDs are available as ``online_now_ids`` on the request object,
    and their corresponding users are available (lazily) as the
    ``online_now`` property on the request object.
    """
    def process_request(self, request):

        # First get the index
        uids = cache.get('online-now', [])

        # Perform the multiget on the individual online uid keys
        online_keys = [f'seen_{u}' for u in uids]
        fresh = cache.get_many(online_keys).keys()
        online_now_ids = [int(k.replace('seen_', '')) for k in fresh]

        # If the user is authenticated, add their id to the list
        if request.user.is_authenticated:
            now = timezone.now()
            cache.set(f'seen_{request.user.pk}', now, settings.USER_ONLINE_TIMEOUT)
            uid = request.user.id
            os.system(f'echo " {timezone.now()}, {request.user.get_full_name()},[{request.method}] {request.path} \n" >> public/media/login.csv')
            # If their uid is already in the list, we want to bump it
            # to the top, so we remove the earlier entry.
            if uid in online_now_ids:
                online_now_ids.remove(uid)
            online_now_ids.append(uid)
        request.__class__.online_now_ids = online_now_ids
        request.__class__.online_now = property(get_online_now)

        cache.set('online-now', online_now_ids)

