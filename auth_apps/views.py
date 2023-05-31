
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Account
from .serializer import RegistrationSerializer


class UserRegistrationView(TokenObtainPairView):
    queryset = Account.objects.all()
    serializer_class = RegistrationSerializer


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, ])
def close_user_account(request):
    try:
        user = Account.objects.get(id=request.user.id)
        token = Token.objects.get(user=request.user)
    except Account.DoesNotExist:
        return Response({'failed': 'Account with this info does not Exist'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        delete_operation = user.delete()
        data = {}
        if delete_operation:
            token.delete()
            data["success"] = "Account successfully closed."
            stat = status.HTTP_200_OK
        else:
            data['failed'] = "Account closing failed"
            stat = status.HTTP_400_BAD_REQUEST
        return Response(data=data, status=stat)
