from django.conf import settings
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone


class LoginRequiredMiddleware(MiddlewareMixin):
    def process_request(self, request):

        exclude_paths = [
            '/logout/','/admin/','/admin/login/'
        ]

        if not request.user.is_authenticated:
            if not request.path == settings.LOGIN_URL:
                if request.path not in exclude_paths:
                    return redirect(settings.LOGIN_URL)

        else:
            if request.path == settings.LOGIN_URL:
                return redirect(settings.INIT_URL)