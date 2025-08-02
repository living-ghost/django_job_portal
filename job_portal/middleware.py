from django.shortcuts import redirect
from django.urls import reverse

class NoCacheMiddleware:
    """
    Middleware to disable caching for all responses.

    This middleware sets the 'Cache-Control', 'Pragma', and 'Expires' headers 
    to prevent caching of responses. It ensures that the client always fetches 
    the latest content from the server.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response


class SkipAdminLoginMiddleware:
    """
    Middleware to redirect unauthenticated users to the admin login page.

    This middleware checks if the user is authenticated. If not, and the user 
    is trying to access the '/admin/index/' path, they will be redirected to 
    the admin login page.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and request.path.startswith('/admin/index/'):
            return redirect('portal_admin_app:admin_login')  # Redirect to admin login page

        response = self.get_response(request)
        return response


class SkipUserLoginMiddleware:
    """
    Middleware to redirect unauthenticated users to the user login page.

    This middleware checks if the user is authenticated. If not, and the user 
    is trying to access the '/user/dashboard/' path, they will be redirected 
    to the user index page.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and request.path.startswith('/user/dashboard/'):
            return redirect('portal_user_app:user_index')  # Redirect to user index page

        response = self.get_response(request)
        return response


class SkipResumeLoginMiddleware:
    """
    Middleware to redirect unauthenticated users to the resume login page.

    This middleware checks if the user is authenticated. If not, and the user 
    is trying to access the '/resume/' path, they will be redirected to the 
    user index page.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and request.path.startswith('/resume/'):
            return redirect('portal_user_app:user_index')  # Redirect to user index page

        response = self.get_response(request)
        return response


class SkipConverterLoginMiddleware:
    """
    Middleware to redirect unauthenticated users to the converter login page.

    This middleware checks if the user is authenticated. If not, and the user 
    is trying to access the '/converter/' path, they will be redirected to the 
    user index page.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and request.path.startswith('/converter/'):
            return redirect('portal_user_app:user_index')  # Redirect to user index page

        response = self.get_response(request)
        return response

class BlockDeletedUserDashboardMiddleware:
    """
    Prevents access to /user/dashboard/ for unauthenticated users (e.g., after account deletion).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Match exact or subpaths under /user/dashboard/
        if request.path.startswith('/user/dashboard/') and not request.user.is_authenticated:
            return redirect('portal_user_app:user_index')

        return self.get_response(request)