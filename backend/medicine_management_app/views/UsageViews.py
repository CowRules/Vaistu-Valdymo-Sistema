from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from medicine_management_app.models import Usage, Dosage
from medicine_management_app.serializers import UsageSerializer, DosageSerializer


@api_view(['GET'])
def usage_list(request):
    queryset = Usage.objects.all()
    serializer = UsageSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def usage_detail(request, pk):
    if not Usage.objects.filter(id=pk).exists():
        return Response({"detail": "Usage not found"}, status=status.HTTP_404_NOT_FOUND)
    queryset = Usage.objects.get(id=pk)
    serializer = UsageSerializer(queryset, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def usage_create(request):
    if request.user.is_authenticated:
        serializer = UsageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"detail": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['PUT'])
def usage_update(request, pk):
    if request.user.is_authenticated:
        if not Usage.objects.filter(id=pk).exists():
            return Response({"detail": "Usage not found"}, status=status.HTTP_404_NOT_FOUND)
        usage = Usage.objects.get(id=pk)
        serializer = UsageSerializer(usage, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"detail": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['DELETE'])
def usage_delete(request, pk):
    if request.user.is_authenticated:
        if not Usage.objects.filter(id=pk).exists():
            return Response({"detail": "Usage not found"}, status=status.HTTP_404_NOT_FOUND)
        medicine = Usage.objects.get(pk=pk)
        medicine.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response({"detail": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def dosage_list(request, pk):
    if not Usage.objects.filter(id=pk).exists():
        return Response({"detail": "Usage not found"}, status=status.HTTP_404_NOT_FOUND)
    usage = Usage.objects.get(id=pk)
    queryset = Dosage.objects.filter(usage=usage)
    serializer = DosageSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
