from datetime import datetime

import jwt
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from users.api.v1.serializers.auth import (
    AuthResponseSerializer,
    CustomTokenObtainPairSerializer,
    LoginRequestSerializer,
    RegisterRequestSerializer,
    UserDataResponseSerializer,
    UserTokenSerializer,
)
from users.api.v1.serializers.user import CustomUserSerializer
from users.models import CustomUser


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        tags=["Authentication"],
        operation_summary="User Registration",
        operation_description="Registers a new user and returns user details.",
        request_body=RegisterRequestSerializer,
        responses={
            201: openapi.Response(
                description="User created successfully",
                schema=UserDataResponseSerializer,
                examples={
                    "application/json": {
                        "message": "User created successfully",
                        "data": {
                            "id": 1,
                            "email": "test@example.com",
                            "first_name": "John",
                            "last_name": "Doe",
                            "contact": "9800000000",
                        },
                    }
                },
            ),
            400: openapi.Response(
                description="Validation Error",
                examples={"application/json": {"message": "Password is required"}},
            ),
        },
    ),
)
class RegisterView(CreateAPIView):
    """Register New User

    Args:
        CreateAPIView (email, first_name, last_name, contact, password): User details
        Creates a new user.

    Returns:
        user: User object
    """

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (AllowAny,)

    @transaction.atomic
    def post(self, request):
        data = request.data.copy()
        password = data.get("password")
        if not password:
            return Response(
                {"message": "Password is required"},
                status=400,
            )
        if isinstance(password, list):
            password = password[0]
        data.pop("password", None)
        serializer = CustomUserSerializer(
            data=data, fields=["email", "first_name", "last_name", "contact"]
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.last_login = datetime.now()
        if self.request.user.is_authenticated and self.request.user.is_admin:
            user.last_login = None
        user.save()
        user.set_password(password)
        user.save()
        return Response(
            {
                "message": "User created successfully",
                "data": CustomUserSerializer(user).data,
            },
            status=201,
        )


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        tags=["Authentication"],
        operation_summary="User Login",
        operation_description="Authenticates user and returns JWT token.",
        request_body=LoginRequestSerializer,
        responses={
            200: openapi.Response(
                description="Successfully logged in",
                schema=AuthResponseSerializer,
                examples={
                    "application/json": {
                        "message": "Successfully logged in",
                        "data": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    }
                },
            ),
            401: openapi.Response(
                description="Invalid credentials",
                examples={"application/json": {"message": "Invalid credentials"}},
            ),
        },
    ),
)
class LoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"message": "Email and password are required."},
                status=400,
            )

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response(
                {"message": "Incorrect email or password"},
                status=401,
            )

        if not user.check_password(password):
            return Response(
                {"message": "Invalid credentials"},
                status=401,
            )

        access_token = CustomTokenObtainPairSerializer.get_token(user)

        user.last_login = timezone.now()
        user.save(update_fields=["last_login"])

        return Response(
            {
                "message": "Successfully logged in",
                "data": access_token,
            },
            status=200,
        )


@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        tags=["Authentication"],
        operation_summary="Get User Data",
        operation_description="Retrieves user data using a provided token.",
        request_body=UserTokenSerializer,
        responses={
            200: openapi.Response(
                description="Successfully fetched user data",
                schema=UserDataResponseSerializer,
                examples={
                    "application/json": {
                        "message": "Successfully fetched user data",
                        "data": {
                            "id": 1,
                            "email": "test@example.com",
                            "first_name": "John",
                            "last_name": "Doe",
                            "contact": "9800000000",
                        },
                    }
                },
            ),
            400: openapi.Response(
                description="Invalid or expired token",
                examples={"application/json": {"message": "Invalid Token"}},
            ),
        },
    ),
)
class GetUserData(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            token = request.data.get("token")
            if not token:
                return Response(
                    {
                        "message": "No token Provided",
                    },
                    status=400,
                )
            try:
                decoded_data = jwt.decode(
                    token,
                    key=settings.SECRET_KEY,
                    algorithms=["HS256"],
                )
            except ExpiredSignatureError:
                return Response(
                    {
                        "message": "Expired Token, Please check the token \
                            and try again",
                    },
                    status=400,
                )
            except InvalidSignatureError:
                return Response(
                    {
                        "message": "Invalid Token, Please check the token \
                            and try again",
                    },
                    status=400,
                )
            exp = datetime.fromtimestamp(decoded_data["exp"])
            if exp < datetime.now():
                return Response(
                    {"message": "Token has expired. Please login again!"},
                    status=400,
                )

            if "user_uuid" not in decoded_data:
                return Response("Invalid Token!")

            try:
                user = CustomUser.objects.get(uuid=decoded_data["user_uuid"])
            except CustomUser.DoesNotExist:
                return Response(
                    {"message": "Invalid Token."},
                    status=400,
                )
            user_data = CustomUserSerializer(user).data
        except Exception as e:
            return Response(
                {
                    "message": str(e),
                },
                status=400,
            )
        return Response(
            {
                "message": "Successfully fetched user data",
                "data": user_data,
            },
            status=200,
        )
