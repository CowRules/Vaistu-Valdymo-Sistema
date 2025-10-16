from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from medicine_management_app.models import Dosage
from medicine_management_app.serializers import DosageSerializer


@api_view(['GET'])
def dosage_detail(request, pk):
    if Dosage.objects.filter(id=pk).exists():
        dosage = Dosage.objects.get(pk=pk)
        serializer = DosageSerializer(dosage, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "Dosage not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def dosage_create(request):
    if request.user.is_authenticated:
        serializer = DosageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"detail": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['PUT'])
def dosage_update(request, pk):
    if request.user.is_authenticated:
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
    else:
        return Response({"detail": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['DELETE'])
def dosage_delete(request, pk):
    if request.user.is_authenticated:
        if not Dosage.objects.filter(id=pk).exists():
            return Response({"detail": "Dosage not found"}, status=status.HTTP_404_NOT_FOUND)
        dosage = Dosage.objects.get(pk=pk)
        if not dosage.usage.medicine.added_by == request.user:
            return Response({"detail": "User does not have permission to delete this dosage"},
                            status=status.HTTP_403_FORBIDDEN)
        dosage.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({"detail": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)