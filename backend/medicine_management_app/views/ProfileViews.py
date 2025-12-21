from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from medicine_management_app.models import Profile
from medicine_management_app.permissions import IsAdminOrClient, IsAdminOrClientOrGuest
from medicine_management_app.schema_utils import DEFAULT_ERROR_RESPONSES
from medicine_management_app.serializers import ProfileSerializer, UserSerializer
from medicine_management_app.token import MyTokenObtainPairSerializer


@extend_schema(
    summary="Get current user profile",
    description="Retrieve the profile of the currently authenticated user.",
    responses={
        200: ProfileSerializer,
        401: DEFAULT_ERROR_RESPONSES[401],
    },
)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminOrClientOrGuest])
def profile_details(request):
    profile = Profile.objects.get(user=request.user)
    serializer = ProfileSerializer(profile)
    return Response(serializer.data, status=status.HTTP_200_OK)

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
@permission_classes([AllowAny])
@authentication_classes([])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.create_user(username=request.data['username'], email=request.data['email'], password=request.data['password'])
        user.save()
        profile = Profile.objects.create(user=user, is_administrator=request.data['is_administrator'], role=request.data['role'])
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
@permission_classes([AllowAny])
@authentication_classes([])
class LoginTokenObtain(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            tokens = response.data
            access_token = tokens['access']
            refresh_token = tokens['refresh']
            res = Response()
            res.data = {'success': True}
            res.set_cookie(
                key='access_token',
                value=str(access_token),
                httponly=True,
                secure=True,
                samesite='None',
                path='/'
            )
            res.set_cookie(
                key='refresh_token',
                value=str(refresh_token),
                httponly=True,
                secure=True,
                samesite='None',
                path='/'
            )
            return res
        except:
            return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    summary="Refresh token",
    description="Refrest access token",
    request=None,
    responses={
        200: OpenApiResponse(description="Token refreshed successfully"),
        400: DEFAULT_ERROR_RESPONSES[400],
    },
)
@permission_classes([AllowAny])
@authentication_classes([])
class RefreshToken(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            request.data['refresh'] = refresh_token
            response = super().post(request, *args, **kwargs)
            tokens = response.data
            access_token = tokens['access']
            res = Response()
            res.data = {'refreshed': True}
            res.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=True,
                samesite='None',
                path='/'
            )
            return res
        except:
            return Response({'refreshed': False}, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    summary="Log out the current user",
    description="Log out the currently authenticated user.",
    responses={
        200: OpenApiResponse(description="User logged out successfully"),
        400: DEFAULT_ERROR_RESPONSES[400],
    },
)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminOrClientOrGuest])
def logout_user(request):
    try:
        res = Response()
        res.data = {'success': True}
        res.delete_cookie('access_token', path='/', samesite='None')
        res.delete_cookie('refresh_token', path='/', samesite='None')
        return res
    except:
        return Response({'success': False}, status=status.HTTP_400_BAD_REQUEST)

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
@permission_classes([IsAuthenticated, IsAdminOrClient])
def update_profile(request):
    profile = Profile.objects.get(user=request.user)
    serializer = ProfileSerializer(data=request.data, instance=profile)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
@permission_classes([IsAuthenticated, IsAdminOrClient])
def change_password(request):
    if "new_password" not in request.POST:
        return Response({'detail': 'New password not provided'}, status=status.HTTP_400_BAD_REQUEST)
    user = request.user
    user.set_password(request.POST["new_password"])
    user.save()
    res = Response({'detail': 'User password changed'}, status=status.HTTP_200_OK)
    res.delete_cookie('access_token', path='/', samesite='None')
    res.delete_cookie('refresh_token', path='/api/refresh', samesite='None')
    return res
