from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse
from medicine_management_app.models import Dosage
from medicine_management_app.permissions import IsAdminOrClientOrGuest, IsAdminOrClient
from medicine_management_app.schema_utils import DEFAULT_ERROR_RESPONSES
from medicine_management_app.serializers import DosageSerializer

@extend_schema(
    summary="Retrieve details of a dosage",
    responses={
        200: DosageSerializer,
        404: DEFAULT_ERROR_RESPONSES[404],
    },
)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminOrClientOrGuest])
def dosage_detail(request, pk):
    if Dosage.objects.filter(id=pk).exists():
        dosage = Dosage.objects.get(pk=pk)
        serializer = DosageSerializer(dosage, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "Dosage not found"}, status=status.HTTP_404_NOT_FOUND)

@extend_schema(
    summary="Create a new dosage entry",
    request=DosageSerializer,
    responses={
        201: DosageSerializer,
        400: DEFAULT_ERROR_RESPONSES[400],
        401: DEFAULT_ERROR_RESPONSES[401],
    },
)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminOrClient])
def dosage_create(request):
    serializer = DosageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    summary="Update an existing dosage",
    request=DosageSerializer,
    responses={
        200: DosageSerializer,
        400: DEFAULT_ERROR_RESPONSES[400],
        401: DEFAULT_ERROR_RESPONSES[401],
        403: DEFAULT_ERROR_RESPONSES[403],
        404: DEFAULT_ERROR_RESPONSES[404],
    },
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminOrClient])
def dosage_update(request, pk):
    if not Dosage.objects.filter(id=pk).exists():
        return Response({"detail": "Dosage not found"}, status=status.HTTP_404_NOT_FOUND)
    dosage = Dosage.objects.get(pk=pk)
    if not dosage.usage.medicine.added_by == request.user:
        return Response({"detail": "User does not have permission to edit this dosage"},
                        status=status.HTTP_403_FORBIDDEN)
    serializer = DosageSerializer(data=request.data, instance=dosage)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    summary="Delete an existing dosage",
    responses={
        204: OpenApiResponse(description="Dosage deleted successfully"),
        401: DEFAULT_ERROR_RESPONSES[401],
        403: DEFAULT_ERROR_RESPONSES[403],
        404: DEFAULT_ERROR_RESPONSES[404],
    },
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminOrClient])
def dosage_delete(request, pk):
    if not Dosage.objects.filter(id=pk).exists():
        return Response({"detail": "Dosage not found"}, status=status.HTTP_404_NOT_FOUND)
    dosage = Dosage.objects.get(pk=pk)
    if not dosage.usage.medicine.added_by == request.user:
        return Response({"detail": "User does not have permission to delete this dosage"},
                        status=status.HTTP_403_FORBIDDEN)
    dosage.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
