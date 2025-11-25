from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from drf_spectacular.utils import extend_schema, OpenApiResponse
from medicine_management_app.models import Medicine, PendingMedicine, Usage
from medicine_management_app.permissions import IsAdminOrClientOrGuest, IsAdminOrClient
from medicine_management_app.schema_utils import DEFAULT_ERROR_RESPONSES
from medicine_management_app.serializers import MedicineSerializer, PendingMedicineSerializer, UsageSerializer

@extend_schema(
    summary="List all medicines",
    responses={200: MedicineSerializer(many=True)},
)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminOrClientOrGuest])
def medicine_list(request):
    medicines = Medicine.objects.all()
    serializer = MedicineSerializer(medicines, many=True)
    return Response(serializer.data)

@extend_schema(
    summary="Retrieve a specific medicine",
    responses={
        200: MedicineSerializer,
        404: DEFAULT_ERROR_RESPONSES[404],
    },
)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminOrClientOrGuest])
def medicine_detail(request, pk):
    if not Medicine.objects.filter(id=pk).exists():
        return Response({"detail": "Medicine not found"}, status=status.HTTP_404_NOT_FOUND)
    medicine = Medicine.objects.get(pk=pk)
    serializer = MedicineSerializer(medicine)
    return Response(serializer.data)

@extend_schema(
    summary="Create a new medicine",
    request=MedicineSerializer,
    responses={
        201: MedicineSerializer,
        400: DEFAULT_ERROR_RESPONSES[400],
        401: DEFAULT_ERROR_RESPONSES[401],
    },
)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminOrClient])
def medicine_create(request):
    serializer = MedicineSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    summary="Update an existing medicine",
    request=MedicineSerializer,
    responses={
        200: MedicineSerializer,
        400: DEFAULT_ERROR_RESPONSES[400],
        401: DEFAULT_ERROR_RESPONSES[401],
        403: DEFAULT_ERROR_RESPONSES[403],
        404: DEFAULT_ERROR_RESPONSES[404],
    },
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminOrClient])
def medicine_update(request, pk):
    if not Medicine.objects.filter(id=pk).exists():
        return Response({"detail": "Medicine not found"}, status=status.HTTP_404_NOT_FOUND)
    medicine = Medicine.objects.get(pk=pk)
    if not medicine.added_by == request.user:
        return Response({"detail": "User does not have permission to edit this medicine"},
                        status=status.HTTP_403_FORBIDDEN)
    serializer = MedicineSerializer(medicine, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    summary="Delete a medicine",
    responses={
        204: OpenApiResponse(description="Deleted successfully"),
        401: DEFAULT_ERROR_RESPONSES[401],
        403: DEFAULT_ERROR_RESPONSES[403],
        404: DEFAULT_ERROR_RESPONSES[404],
    },
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminOrClient])
def medicine_delete(request, pk):
    if not Medicine.objects.filter(id=pk).exists():
        return Response({"detail": "Medicine not found"}, status=status.HTTP_404_NOT_FOUND)
    medicine = Medicine.objects.get(pk=pk)
    if not medicine.added_by == request.user:
        return Response({"detail": "User does not have permission to edit this medicine"},
                        status=status.HTTP_403_FORBIDDEN)
    medicine.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@extend_schema(
    summary="List all pending medicines",
    responses={200: PendingMedicineSerializer(many=True)},
)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminOrClientOrGuest])
def pending_medicine_list(request):
    pending_medicine = PendingMedicine.objects.all()
    serializer = PendingMedicineSerializer(pending_medicine, many=True)
    return Response(serializer.data)

@extend_schema(
    summary="Retrieve details of a pending medicine",
    responses={
        200: PendingMedicineSerializer,
        404: DEFAULT_ERROR_RESPONSES[404],
    },
)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminOrClientOrGuest])
def pending_medicine_detail(request, pk):
    if not PendingMedicine.objects.filter(id=pk).exists():
        return Response({"detail": "Pending medicine not found"}, status=status.HTTP_404_NOT_FOUND)
    pending_medicine = PendingMedicine.objects.get(pk=pk)
    serializer = PendingMedicineSerializer(pending_medicine)
    return Response(serializer.data)

@extend_schema(
    summary="Submit a pending medicine for approval",
    request=PendingMedicineSerializer,
    responses={
        201: PendingMedicineSerializer,
        400: DEFAULT_ERROR_RESPONSES[400],
        401: DEFAULT_ERROR_RESPONSES[401],
    },
)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminOrClient])
def pending_medicine_create(request):
    try:
        medicine = Medicine.objects.get(id=request.data['medicine_id'], added_by=request.user)
        if medicine.is_global is not True:
            pending_medicine = PendingMedicine.objects.create(medicine=medicine, comments=request.data['comment'])
            pending_medicine.save()
            serializer = PendingMedicineSerializer(pending_medicine)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    except Medicine.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    summary="Update a pending medicine",
    request=PendingMedicineSerializer,
    responses={
        200: PendingMedicineSerializer,
        400: DEFAULT_ERROR_RESPONSES[400],
        401: DEFAULT_ERROR_RESPONSES[401],
        403: DEFAULT_ERROR_RESPONSES[403],
        404: DEFAULT_ERROR_RESPONSES[404],
    },
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminOrClient])
def pending_medicine_update(request, pk):
    if not PendingMedicine.objects.filter(id=pk).exists():
        return Response({"detail": "Pending medicine not found"}, status=status.HTTP_404_NOT_FOUND)
    pending_medicine = PendingMedicine.objects.get(pk=pk)
    user = User.objects.get(pk=request.user.id)
    if not pending_medicine.medicine.added_by == request.user and user.profile.is_administrator is False:
        return Response({"detail": "User does not have permission to edit this pending medicine"},
                        status=status.HTTP_403_FORBIDDEN)
    serializer = PendingMedicineSerializer(pending_medicine, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    summary="List usages for a specific medicine",
    responses={
        200: UsageSerializer(many=True),
        404: DEFAULT_ERROR_RESPONSES[404],
    },
)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminOrClientOrGuest])
def medicine_usage(request, pk):
    if not Medicine.objects.filter(id=pk).exists():
        return Response({"detail": "Medicine not found"}, status=status.HTTP_404_NOT_FOUND)
    medicine = Medicine.objects.get(pk=pk)
    usages = Usage.objects.filter(medicine=medicine)
    serializer = UsageSerializer(usages, many=True)
    return Response(serializer.data)