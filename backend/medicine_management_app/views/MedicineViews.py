from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from medicine_management_app.models import Medicine, PendingMedicine, Usage
from medicine_management_app.serializers import MedicineSerializer, PendingMedicineSerializer, UsageSerializer


@api_view(['GET'])
def medicine_list(request):
    medicines = Medicine.objects.all()
    serializer = MedicineSerializer(medicines, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def medicine_detail(request, pk):
    if not Medicine.objects.filter(id=pk).exists():
        return Response({"detail": "Medicine not found"}, status=status.HTTP_404_NOT_FOUND)
    medicine = Medicine.objects.get(pk=pk)
    serializer = MedicineSerializer(medicine)
    return Response(serializer.data)

@api_view(['POST'])
def medicine_create(request):
    if request.user.is_authenticated:
        serializer = MedicineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"detail": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['PUT'])
def medicine_update(request, pk):
    if request.user.is_authenticated:
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
    else:
        return Response({"detail": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['DELETE'])
def medicine_delete(request, pk):
    if request.user.is_authenticated:
        if not Medicine.objects.filter(id=pk).exists():
            return Response({"detail": "Medicine not found"}, status=status.HTTP_404_NOT_FOUND)
        medicine = Medicine.objects.get(pk=pk)
        if not medicine.added_by == request.user:
            return Response({"detail": "User does not have permission to edit this medicine"},
                            status=status.HTTP_403_FORBIDDEN)
        medicine.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({"detail": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def pending_medicine_list(request):
    pending_medicine = PendingMedicine.objects.all()
    serializer = PendingMedicineSerializer(pending_medicine, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def pending_medicine_detail(request, pk):
    if not PendingMedicine.objects.filter(id=pk).exists():
        return Response({"detail": "Pending medicine not found"}, status=status.HTTP_404_NOT_FOUND)
    pending_medicine = PendingMedicine.objects.get(pk=pk)
    serializer = PendingMedicineSerializer(pending_medicine)
    return Response(serializer.data)

@api_view(['POST'])
def pending_medicine_create(request):
    try:
        if request.user.is_authenticated:
            medicine = Medicine.objects.get(id=request.data['medicine_id'], added_by=request.user)
            if medicine.is_global is not True:
                pending_medicine = PendingMedicine.objects.create(medicine=medicine, comments=request.data['comment'])
                pending_medicine.save()
                serializer = PendingMedicineSerializer(pending_medicine)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
    except Medicine.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def pending_medicine_update(request, pk):
    if request.user.is_authenticated:
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
    else:
        return Response({"detail": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def medicine_usage(request, pk):
    if not Medicine.objects.filter(id=pk).exists():
        return Response({"detail": "Medicine not found"}, status=status.HTTP_404_NOT_FOUND)
    medicine = Medicine.objects.get(pk=pk)
    usages = Usage.objects.filter(medicine=medicine)
    serializer = UsageSerializer(usages, many=True)
    return Response(serializer.data)