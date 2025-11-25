from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse
from medicine_management_app.models import Category, Medicine, Profile
from medicine_management_app.permissions import IsAdminOrClientOrGuest, IsAdmin
from medicine_management_app.schema_utils import DEFAULT_ERROR_RESPONSES
from medicine_management_app.serializers import CategorySerializer, CategoriesSerializer, MedicineSerializer

@extend_schema(
    summary="List all categories",
    description="Retrieve a list of all available medicine categories.",
    responses={200: CategoriesSerializer(many=True)},
)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminOrClientOrGuest])
def categories_list(request):
    queryset = Category.objects.all()
    serializer = CategoriesSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(
    summary="Retrieve category details",
    description="Retrieve details of a specific category. Only accessible to administrators.",
    responses={
        200: CategorySerializer,
        401: DEFAULT_ERROR_RESPONSES[401],
        403: DEFAULT_ERROR_RESPONSES[403],
        404: DEFAULT_ERROR_RESPONSES[404],
    },
)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdmin])
def category_detail(request, pk):
    if Category.objects.filter(id=pk).exists():
        queryset = Category.objects.prefetch_related('medicines').get(id=pk)
        serializer = CategorySerializer(queryset, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

@extend_schema(
    summary="Create a new category",
    description="Create a new medicine category. Administrator-only endpoint.",
    request=CategorySerializer,
    responses={
        201: CategorySerializer,
        400: DEFAULT_ERROR_RESPONSES[400],
        401: DEFAULT_ERROR_RESPONSES[401],
        403: DEFAULT_ERROR_RESPONSES[403],
    },
)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdmin])
def category_create(request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    summary="Update a category",
    description="Update an existing category. Administrator-only endpoint.",
    request=CategorySerializer,
    responses={
        200: CategorySerializer,
        400: DEFAULT_ERROR_RESPONSES[400],
        401: DEFAULT_ERROR_RESPONSES[401],
        403: DEFAULT_ERROR_RESPONSES[403],
        404: DEFAULT_ERROR_RESPONSES[404],
    },
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdmin])
def category_update(request, pk):
    if Category.objects.filter(id=pk).exists():
        queryset = Category.objects.get(pk=pk)
        serializer = CategorySerializer(queryset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"detail": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

@extend_schema(
    summary="Delete a category",
    description="Delete a specific category. Administrator-only endpoint.",
    responses={
        204: OpenApiResponse(description="Category deleted successfully."),
        401: DEFAULT_ERROR_RESPONSES[401],
        403: DEFAULT_ERROR_RESPONSES[403],
        404: DEFAULT_ERROR_RESPONSES[404],
    },
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdmin])
def category_delete(request, pk):
    if Category.objects.filter(id=pk).exists():
        queryset = Category.objects.get(pk=pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({"detail": "Category not found"}, status=status.HTTP_404_NOT_FOUND)

@extend_schema(
    summary="List medicines in a category",
    description="Retrieve all medicines belonging to a specific category.",
    responses={
        200: MedicineSerializer(many=True),
        404: DEFAULT_ERROR_RESPONSES[404],
    },
)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminOrClientOrGuest])
def category_medicine(request, pk):
    if Category.objects.filter(id=pk).exists():
        category = Category.objects.get(pk=pk)
        queryset = Medicine.objects.filter(categories=category)
        serializer = MedicineSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "Category not found"}, status=status.HTTP_404_NOT_FOUND)
