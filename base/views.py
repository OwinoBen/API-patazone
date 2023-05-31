from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import AddressSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_customer_address(request):
    reqBody = request.data
    use_id = reqBody['user_id']
    if request.method == 'POST':

        data = request.data
        serializer = AddressSerializer(data=data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Address added successfully", "data": serializer.data},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
