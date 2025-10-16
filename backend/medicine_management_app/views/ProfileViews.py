from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse
from medicine_management_app.models import Profile
from medicine_management_app.schema_utils import DEFAULT_ERROR_RESPONSES
from medicine_management_app.serializers import ProfileSerializer, UserSerializer

@extend_schema(
    summary="Get current user profile",
    description="Retrieve the profile of the currently authenticated user.",
    responses={
        200: ProfileSerializer,
        401: DEFAULT_ERROR_RESPONSES[401],
    },
)
@api_view(['GET'])
def profile_details(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'detail': "User unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

@extend_schema(
    summary="Register a new user",
    description="Create a new user account along with a profile.",
    request=UserSerializer,
    responses={
        201: OpenApiResponse(description="User created successfully"),
        400: DEFAULT_ERROR_RESPONSES[400],
    },
)
@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.create_user(username=request.data['username'], email=request.data['email'], password=request.data['password'])
        user.save()
        profile = Profile.objects.create(user=user)
        profile.save()
        return Response({'detail': 'User created'}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    summary="Log in a user",
    description="Authenticate a user with username and password.",
    request=None,
    responses={
        200: OpenApiResponse(description="User logged in successfully"),
        400: DEFAULT_ERROR_RESPONSES[400],
    },
)
@api_view(['POST'])
def login_user(request):
    if "username" not in request.POST or "password" not in request.POST:
        return Response({'detail': "Username and password is required"}, status=status.HTTP_400_BAD_REQUEST)
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({'detail': 'User logged in'}, status=status.HTTP_200_OK)
    else:
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    summary="Log out the current user",
    description="Log out the currently authenticated user.",
    responses={
        200: OpenApiResponse(description="User logged out successfully"),
        400: DEFAULT_ERROR_RESPONSES[400],
    },
)
@api_view(['POST'])
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return Response({'detail': 'User logged out'}, status=status.HTTP_200_OK)
    else:
        return Response({'detail': 'User is not logged in'}, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    summary="Update user profile",
    description="Update the profile of the currently authenticated user.",
    request=ProfileSerializer,
    responses={
        200: ProfileSerializer,
        400: DEFAULT_ERROR_RESPONSES[400],
        401: DEFAULT_ERROR_RESPONSES[401],
    },
)
@api_view(['PUT'])
def update_profile(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(data=request.data, instance=profile)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'detail': "User unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

@extend_schema(
    summary="Change user password",
    description="Change the password of the currently authenticated user.",
    request=None,
    responses={
        200: OpenApiResponse(description="Password changed successfully"),
        400: DEFAULT_ERROR_RESPONSES[400],
        401: DEFAULT_ERROR_RESPONSES[401],
    },
)
@api_view(['PUT'])
def change_password(request):
    if "new_password" not in request.POST:
        return Response({'detail': 'New password not provided'}, status=status.HTTP_400_BAD_REQUEST)
    if request.user.is_authenticated:
        user = request.user
        user.set_password(request.POST["new_password"])
        user.save()
        return Response({'detail': 'User password changed'}, status=status.HTTP_200_OK)
    else:
        return Response({'detail': 'User is not logged in'}, status=status.HTTP_400_BAD_REQUEST)
