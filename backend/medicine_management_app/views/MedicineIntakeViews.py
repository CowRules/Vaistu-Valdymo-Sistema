import time
from datetime import datetime, time
from django.utils import timezone
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from medicine_management_app.models import MedicineIntake, Dosage
from medicine_management_app.permissions import IsAdminOrClient
from medicine_management_app.schema_utils import DEFAULT_ERROR_RESPONSES
from medicine_management_app.serializers import MedicineIntakeSerializer

@extend_schema(
    summary="List all medicine intakes for the authenticated user",
    responses={
        200: MedicineIntakeSerializer(many=True),
        401: DEFAULT_ERROR_RESPONSES[401],
    },
)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminOrClient])
def medicine_intake_list(request):
    medicine_intakes = MedicineIntake.objects.filter(user=request.user)
    serializer = MedicineIntakeSerializer(medicine_intakes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(
    summary="Retrieve details of a medicine intake",
    responses={
        200: MedicineIntakeSerializer,
        401: DEFAULT_ERROR_RESPONSES[401],
        403: DEFAULT_ERROR_RESPONSES[403],
        404: DEFAULT_ERROR_RESPONSES[404],
    },
)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminOrClient])
def medicine_intake_detail(request, pk):
    if not MedicineIntake.objects.filter(id=pk).exists():
        return Response({"detail": "Medicine intake not found"}, status=status.HTTP_404_NOT_FOUND)
    medicine_intake = MedicineIntake.objects.get(id=pk)
    if not medicine_intake.user == request.user:
        return Response({"detail": "User does not have permission to view this medicine intake"},
                        status=status.HTTP_403_FORBIDDEN)
    serializer = MedicineIntakeSerializer(medicine_intake)
    return Response(serializer.data, status=status.HTTP_200_OK)

@extend_schema(
    summary="Create a new medicine intake",
    request=MedicineIntakeSerializer,
    responses={
        201: MedicineIntakeSerializer,
        400: DEFAULT_ERROR_RESPONSES[400],
        401: DEFAULT_ERROR_RESPONSES[401],
    },
)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminOrClient])
def medicine_intake_create(request):
    serializer = MedicineIntakeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    summary="Update a medicine intake",
    request=MedicineIntakeSerializer,
    responses={
        200: MedicineIntakeSerializer,
        400: DEFAULT_ERROR_RESPONSES[400],
        401: DEFAULT_ERROR_RESPONSES[401],
        403: DEFAULT_ERROR_RESPONSES[403],
        404: DEFAULT_ERROR_RESPONSES[404],
    },
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminOrClient])
def medicine_intake_update(request, pk):
    if not MedicineIntake.objects.filter(id=pk).exists():
        return Response({"detail": "Medicine intake not found"}, status=status.HTTP_404_NOT_FOUND)
    medicine_intake = MedicineIntake.objects.get(pk=pk)
    if not medicine_intake.user == request.user:
        return Response({"detail": "User does not have permission to edit this medicine intake"},
                        status=status.HTTP_403_FORBIDDEN)
    serializer = MedicineIntakeSerializer(medicine_intake, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    summary="Delete a medicine intake",
    responses={
        204: OpenApiResponse(description="Medicine intake deleted successfully"),
        401: DEFAULT_ERROR_RESPONSES[401],
        403: DEFAULT_ERROR_RESPONSES[403],
        404: DEFAULT_ERROR_RESPONSES[404],
    },
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminOrClient])
def medicine_intake_delete(request, pk):
    if not MedicineIntake.objects.filter(id=pk).exists():
        return Response({"detail": "Medicine intake not found"}, status=status.HTTP_404_NOT_FOUND)
    medicine_intake = MedicineIntake.objects.get(pk=pk)
    if not medicine_intake.user == request.user:
        return Response({"detail": "User does not have permission to edit this medicine intake"},
                        status=status.HTTP_403_FORBIDDEN)
    medicine_intake.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@extend_schema(
    summary="Retrieve medicine that should be taken right now",
    description="Checks what time of the day it is and retrieves medicine intakes which have a dosage set for "
                "the current time of the day and medicine has not been consumed today on this time period.",
    responses={
        200: MedicineIntakeSerializer(many=True),
        401: DEFAULT_ERROR_RESPONSES[401],
    },
)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminOrClient])
def retrieve_medicine_past_consumption_time(request):
    medicine_intakes = MedicineIntake.objects.filter(user=request.user)
    now = datetime.now().time()
    morning = (time(6, 0), time(12, 0))
    afternoon = (time(12, 0), time(17, 0))
    evening = (time(17, 0), time(21, 0))
    night = (time(21, 0), time(23, 59))
    today = datetime.today().date()
    if morning[0] <= now < morning[1]:
        specified_time = time(6, 0)
        start_time = datetime.combine(today, specified_time)
        medicine_intakes = medicine_intakes.filter(usage__dosage__time="Morning", morning_time__lte=now, last_intake__lt=start_time)
    elif afternoon[0] <= now < afternoon[1]:
        specified_time = time(12, 0)
        start_time = datetime.combine(today, specified_time)
        medicine_intakes = medicine_intakes.filter(usage__dosage__time="Afternoon", afternoon_time__lte=now, last_intake__lt=start_time)
    elif evening[0] <= now < evening[1]:
        specified_time = time(17, 0)
        start_time = datetime.combine(today, specified_time)
        medicine_intakes = medicine_intakes.filter(usage__dosage__time="Evening", evening_time__lte=now, last_intake__lt=start_time)
    elif night[0] <= now < night[1]:
        specified_time = time(21, 0)
        start_time = datetime.combine(today, specified_time)
        medicine_intakes = medicine_intakes.filter(usage__dosage__time="Night", night_time__lte=now, last_intake__lt=start_time)
    else:
        return Response(status=status.HTTP_200_OK)

    serializer = MedicineIntakeSerializer(medicine_intakes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
