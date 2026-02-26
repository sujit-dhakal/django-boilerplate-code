# This includes version 1 (v1) apis for the app
            from django.urls import path, include
            from rest_framework.routers import DefaultRouter

            router = DefaultRouter()
            # Register your viewsets here
            # router.register(r'example', views.ExampleViewSet)

            urlpatterns = [
                path('', include(router.urls)),
                # Add your additional version 1 API endpoints here
            ]
            