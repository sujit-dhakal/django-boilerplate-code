import threading

from django.contrib.auth.models import AnonymousUser


class CuserMiddleware:
    """
    Always have access to the current user
    """

    _storage = threading.local()

    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        self.__class__.set_request(request)
        response = self.get_response(request)

        self.__class__.del_request()
        self.__class__.del_user()
        return response

    @classmethod
    def get_user(cls, default=None):
        """
        Retrieve user info
        """
        user = getattr(cls._storage, "user", None)
        if user and not isinstance(user, AnonymousUser):
            return user

        request = getattr(cls._storage, "request", None)
        if request:
            user = getattr(request, "user", None)
            if user and not isinstance(user, AnonymousUser):
                return user
        return default

    @classmethod
    def set_user(cls, user):
        """
        Store user info
        """
        cls._storage.user = user

    @classmethod
    def del_user(cls):
        """
        Delete user info
        """
        if hasattr(cls._storage, "user"):
            del cls._storage.user

    @classmethod
    def get_request(cls):
        """
        Retrieve request info
        """
        return getattr(cls._storage, "request", None)

    @classmethod
    def set_request(cls, request):
        """
        Store request info
        """
        cls._storage.request = request

    @classmethod
    def del_request(cls):
        """
        Delete request info
        """
        if hasattr(cls._storage, "request"):
            del cls._storage.request
