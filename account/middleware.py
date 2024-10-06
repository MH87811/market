from django.shortcuts import redirect
from django.http import HttpResponse

class EmailVerificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.user.verified:
            return HttpResponse('email_verification_required')
        response = self.get_response(request)
        return response