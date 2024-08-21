from django.shortcuts import redirect
from django.urls import reverse


class NoCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response

class SkipAdminLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # If the user is not authenticated and trying to access a specific path
        if not request.user.is_authenticated and request.path.startswith('/admin/index/'):
            return redirect('portal_admin_app:admin_login')  # Redirect to a different page

        response = self.get_response(request)
        return response
    
class SkipUserLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # If the user is not authenticated and trying to access a specific path
        if not request.user.is_authenticated and request.path.startswith('/user/dashboard/'):
            return redirect('portal_user_app:user_index')  # Redirect to a different page

        response = self.get_response(request)
        return response
    
class SkipResumeLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # If the user is not authenticated and trying to access a specific path
        if not request.user.is_authenticated and request.path.startswith('/resume/'):
            return redirect('portal_user_app:user_index')  # Redirect to a different page

        response = self.get_response(request)
        return response
    
class SkipConverterLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # If the user is not authenticated and trying to access a specific path
        if not request.user.is_authenticated and request.path.startswith('/converter/'):
            return redirect('portal_user_app:user_index')  # Redirect to a different page

        response = self.get_response(request)
        return response