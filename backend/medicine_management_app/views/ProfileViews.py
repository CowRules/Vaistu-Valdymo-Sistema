from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from medicine_management_app.models import Profile
from medicine_management_app.serializers import ProfileSerializer, UserSerializer


@api_view(['GET'])
def profile_details(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'detail': "User unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

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

@api_view(['POST'])
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return Response({'detail': 'User logged out'}, status=status.HTTP_200_OK)
    else:
        return Response({'detail': 'User is not logged in'}, status=status.HTTP_400_BAD_REQUEST)

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
