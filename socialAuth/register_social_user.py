import os

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

from auth_apps.models import Account


def register_social_user(provider, user_id, email, firstname, lastname):
    data = {}
    try:
        filter_userby_email = Account.objects.get(email=email)
        token = Token.objects.get_or_create(user=filter_userby_email)[0].key
        if provider == filter_userby_email.auth_provider:
            registered_user = authenticate(
                email=email, password=os.getenv('SOCIAL_SECRET'))
            data["message"] = "user logged in"
            data["email_address"] = registered_user.email
            Res = {"data": data, "token": token}
            return Res
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

        data['message'] = 'Thank you for joining patazone!'
        data['email'] = new_user.email
        data['firstname'] = new_user.firstname
        data['lastname'] = new_user.lastname
        token = Token.objects.get(user=user).key
        return {"data": data, "token": token}

