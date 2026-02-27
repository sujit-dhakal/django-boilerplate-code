from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.api.v1.views.authentication import GetUserData, LoginView, RegisterView

router = DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/me/", GetUserData.as_view(), name="get_user"),
]
