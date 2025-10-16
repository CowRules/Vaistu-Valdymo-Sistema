from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from medicine_management_app.models import Category, Medicine, Profile
from medicine_management_app.serializers import CategorySerializer, CategoriesSerializer, MedicineSerializer


@api_view(['GET'])
def categories_list(request):
    queryset = Category.objects.all()
    serializer = CategoriesSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def category_detail(request, pk):
    if request.user.is_authenticated:
        if Profile.objects.get(user=request.user).is_administrator is False:
            return Response({"detail": "User does not have permission to view this page."},
                            status=status.HTTP_403_FORBIDDEN)
        if Category.objects.filter(id=pk).exists():
            queryset = Category.objects.prefetch_related('medicines').get(id=pk)
            serializer = CategorySerializer(queryset, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"detail": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def category_create(request):
    if request.user.is_authenticated:
        if Profile.objects.get(user=request.user).is_administrator is False:
            return Response({"detail": "User does not have permission to create new categories."},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"detail": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['PUT'])
def category_update(request, pk):
    if request.user.is_authenticated:
        if Profile.objects.get(user=request.user).is_administrator is False:
            return Response({"detail": "User does not have permission to update new categories."},
                            status=status.HTTP_403_FORBIDDEN)
        if Category.objects.filter(id=pk).exists():
            queryset = Category.objects.get(pk=pk)
            serializer = CategorySerializer(queryset, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"detail": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['DELETE'])
def category_delete(request, pk):
    if request.user.is_authenticated:
        if Profile.objects.get(user=request.user).is_administrator is False:
            return Response({"detail": "User does not have permission to delete new categories."},
                            status=status.HTTP_403_FORBIDDEN)
        if Category.objects.filter(id=pk).exists():
            queryset = Category.objects.get(pk=pk)
            queryset.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"detail": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def category_medicine(request, pk):
    if Category.objects.filter(id=pk).exists():
        category = Category.objects.get(pk=pk)
        queryset = Medicine.objects.filter(categories=category)
        serializer = MedicineSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
