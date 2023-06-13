import os

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from api import settings
from auth_apps.models import Account
from utils.messages.hundle_messages import successResponse


def register_social_user(provider, email, firstname, lastname):
    data = {}

    try:
        filter_userby_email = Account.objects.get(email=email)
        token = Token.objects.get_or_create(user=filter_userby_email)[0].key
        if provider == filter_userby_email.auth_provider:
            authenticate(
                email=email, password=os.getenv('SOCIAL_SECRET'))
            tokens = RefreshToken.for_user(filter_userby_email)

            data["message"] = "user logged in"
            data['new_user'] = False
            Res = {
                "data": data,
                "token": {
                    "refresh": str(tokens),
                    "access": str(tokens.access_token)
                },
                "expires_in": settings.SIMPLE_JWT.get('ACCESS_TOKEN_LIFETIME')
            }

            return successResponse(status_code=status.HTTP_200_OK, message_code="authentication",
                                   message=Res)
        else:
            raise AuthenticationFailed(detail='Please continue using ' + filter_userby_email.auth_provider)
    except Account.DoesNotExist:
        user = Account(
            email=email,
            firstname=firstname,
            lastname=lastname,
            phone='',
        )
        user.set_password(os.getenv('SOCIAL_SECRET'))
        user.auth_provider = provider
        user.save()
        new_user = authenticate(email=email, password=os.getenv('SOCIAL_SECRET'))
        tokens = RefreshToken.for_user(user)
        data['message'] = 'Welcome to Patazone!'
        data['new_user'] = True
        Res = {
            "data": data,
            "token": {
                "refresh": str(tokens),
                "access": str(tokens.access_token)
            },
            "expires_in": settings.SIMPLE_JWT.get('ACCESS_TOKEN_LIFETIME')
        }
        token = Token.objects.get(user=user).key
        return successResponse(status_code=status.HTTP_200_OK, message_code="authentication",
                               message=Res)
