
from django.shortcuts import render
from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from auth_apps.models import PtzAccountUsers
from auth_apps.serializer import UserSerializer
from .models import PtzAddress
from .serializers import AddressSerializer


# Create your views here.

def index(request):
    users = PtzAccountUsers.objects.all()

    context = {
        'users': users
    }
    return render(request, 'index.html', context)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def getAccountUsers(request):
    try:
        users = PtzAccountUsers.objects.all()
    except PtzAccountUsers.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def saveCustomerAddress(request):
    reqBody = request.data
    # email1 = reqBody['email']
    use_id = reqBody['user_id']
    if request.method == 'POST':
        # data = JSONParser().parse(request)
        # if PtzAddress.objects.filter(user_id=use_id).exists():
        #     return Response({"error": "Your shipping address already exists"}, status=status.HTTP_400_BAD_REQUEST)
        data = request.data
        serializer = AddressSerializer(data=data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Address added successfully", "data": serializer.data},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAddressList(request):
    try:
        address = PtzAddress.objects.filter(user_id=request.user.id)
    except PtzAddress.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = AddressSerializer(address, many=True)
        return Response({"results": serializer.data}, status=status.HTTP_200_OK)
