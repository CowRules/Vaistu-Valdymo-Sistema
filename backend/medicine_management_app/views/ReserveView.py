from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from medicine_management_app.models import Reserve, ReserveMedicine, ReserveActivity
from medicine_management_app.serializers import ReserveSerializer, ReserveMedicineSerializer, ReserveActivitySerializer


@api_view(['GET'])
def reserve_list(request):
    if request.user.is_authenticated:
        reserves = Reserve.objects.filter(user=request.user)
        serializer = ReserveSerializer(reserves, many=True)
        return Response(serializer.data)
    else:
        return Response({"detail": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def reserve_detail(request, pk):
    if request.user.is_authenticated:
        if not Reserve.objects.filter(id=pk).exists():
            return Response({"detail": "Reserve not found"}, status=status.HTTP_404_NOT_FOUND)
        reserve = Reserve.objects.get(pk=pk)
        if not reserve.user == request.user:
            return Response({"detail": "User does not have access to this reserve"},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = ReserveSerializer(reserve)
        return Response(serializer.data)
    else:
        return Response({"detail": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def reserve_create(request):
    if request.user.is_authenticated:
        serializer = ReserveSerializer(data=request.data)
        if serializer.is_valid():
            reserve = Reserve.objects.create(name=request.data["name"], user=request.user)
            reserve.save()
            return Response(ReserveSerializer(reserve).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"detail": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['PUT'])
def reserve_update(request, pk):
    if request.user.is_authenticated:
        if not Reserve.objects.filter(id=pk).exists():
            return Response({"detail": "Reserve not found"}, status=status.HTTP_404_NOT_FOUND)
        reserve = Reserve.objects.get(pk=pk)
        if not reserve.user == request.user:
            return Response({"detail": "User does not have access to this reserve"},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = ReserveSerializer(data=request.data, instance=reserve)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"detail": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['DELETE'])
def reserve_delete(request, pk):
    if request.user.is_authenticated:
        if not Reserve.objects.filter(id=pk).exists():
            return Response({"detail": "Reserve not found"}, status=status.HTTP_404_NOT_FOUND)
        reserve = Reserve.objects.get(pk=pk)
        if not reserve.user == request.user:
            return Response({"detail": "User does not have access to this reserve"},
                            status=status.HTTP_403_FORBIDDEN)
        reserve.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({"detail": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def reserve_medicine_list(request, pk):
    if request.user.is_authenticated:
        if not Reserve.objects.filter(id=pk).exists():
            return Response({"detail": "Reserve not found"}, status=status.HTTP_404_NOT_FOUND)
        reserve = Reserve.objects.get(pk=pk)
        if not reserve.user == request.user:
            return Response({"detail": "User does not have access to this reserve"},
                            status=status.HTTP_403_FORBIDDEN)
        reserve_medicine = ReserveMedicine.objects.filter(reserve=reserve)
        serializer = ReserveMedicineSerializer(reserve_medicine, many=True)
        return Response(serializer.data)
    else:
        return Response({"detail": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def reserve_medicine_detail(request, pk, med_pk):
    if request.user.is_authenticated:
        if not Reserve.objects.filter(id=pk).exists():
            return Response({"detail": "Reserve not found"}, status=status.HTTP_404_NOT_FOUND)
        reserve = Reserve.objects.get(pk=pk)
        if not reserve.user == request.user:
            return Response({"detail": "User does not have access to this reserve"},
                            status=status.HTTP_403_FORBIDDEN)
        if not ReserveMedicine.objects.filter(pk=med_pk, reserve=reserve).exists():
            return Response({"detail": "Reserve medicine not found"}, status=status.HTTP_404_NOT_FOUND)
        reserve_medicine = ReserveMedicine.objects.get(pk=med_pk, reserve=reserve)
        serializer = ReserveMedicineSerializer(reserve_medicine)
        return Response(serializer.data)
    else:
        return Response({"detail": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def reserve_medicine_add(request):
    if request.user.is_authenticated:
        serializer = ReserveMedicineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"detail": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['PUT'])
def reserve_medicine_update(request, pk, med_pk):
    if request.user.is_authenticated:
        if not Reserve.objects.filter(id=pk).exists():
            return Response({"detail": "Reserve not found"}, status=status.HTTP_404_NOT_FOUND)
        reserve = Reserve.objects.get(pk=pk)
        if not reserve.user == request.user:
            return Response({"detail": "User does not have access to this reserve"},
                            status=status.HTTP_403_FORBIDDEN)
        if not ReserveMedicine.objects.filter(pk=med_pk, reserve=reserve).exists():
            return Response({"detail": "Reserve medicine not found"}, status=status.HTTP_404_NOT_FOUND)
        reserve_medicine = ReserveMedicine.objects.get(pk=med_pk, reserve=reserve)
        serializer = ReserveMedicineSerializer(data=request.data, instance=reserve_medicine)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"detail": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['PUT'])
def reserve_medicine_consume(request, pk, med_pk):
    if request.user.is_authenticated:
        if not Reserve.objects.filter(id=pk).exists():
            return Response({"detail": "Reserve not found"}, status=status.HTTP_404_NOT_FOUND)
        reserve = Reserve.objects.get(pk=pk)
        if not reserve.user == request.user:
            return Response({"detail": "User does not have access to this reserve"},
                            status=status.HTTP_403_FORBIDDEN)
        if not ReserveMedicine.objects.filter(pk=med_pk, reserve=reserve).exists():
            return Response({"detail": "Reserve medicine not found"}, status=status.HTTP_404_NOT_FOUND)
        reserve_medicine = ReserveMedicine.objects.get(pk=med_pk, reserve=reserve)
        if reserve_medicine.amount < request.data['amount']:
            return Response({"detail": "Insufficient amount"},status=status.HTTP_400_BAD_REQUEST)
        else:
            reserve_activity = ReserveActivity.objects.create(reserve_medicine=reserve_medicine, consumed_amount=request.data['amount'])
            reserve_activity.save()
            reserve_medicine.amount = reserve_medicine.amount - request.data['amount']
            reserve_medicine.save()
            return Response(status=status.HTTP_200_OK)
    else:
        return Response({"detail": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def reserve_activity_details(request, pk):
    if request.user.is_authenticated:
        if not Reserve.objects.filter(id=pk).exists():
            return Response({"detail": "Reserve not found"}, status=status.HTTP_404_NOT_FOUND)
        reserve = Reserve.objects.get(pk=pk)
        if not reserve.user == request.user:
            return Response({"detail": "User does not have access to this reserve"},
                            status=status.HTTP_403_FORBIDDEN)
        reserve_activity = ReserveActivity.objects.filter(reserve_medicine__reserve=reserve)
        serializer = ReserveActivitySerializer(reserve_activity, many=True)
        return Response(serializer.data)
    else:
        return Response({"detail": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
