from django.urls import include, path

urlpatterns = [
    path("api/v1/users/", include("users.api.v1.urls")),
]
