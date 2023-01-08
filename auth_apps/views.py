import json

import requests
from braces.views import CsrfExemptMixin
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.hashers import check_password
from datetime import datetime

from django.db import transaction
from django.shortcuts import render

# Create your views here.
from oauth2_provider.models import AccessToken, Application, RefreshToken
from oauth2_provider.settings import oauth2_settings
from oauth2_provider.views.mixins import OAuthLibMixin
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PtzAccountUsers, Account
from .serializer import UserSerializer, RegistrationSerializer, AccountPropertiesSerializer, RegisterSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'Registration successful!'
            data['email'] = account.email
            data['firstname'] = account.firstname
            data['lastname'] = account.lastname
            data['phone'] = account.phone
            # data['username'] = account.username
            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def account_property_view(request):
    try:
        acount = request.user
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AccountPropertiesSerializer(acount)
        return Response(serializer.data)


@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def update_account_view(request):
    try:
        acount = request.user
    except Account.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        serializer = AccountPropertiesSerializer(acount, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = "Account successfullY updated"
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# user login with token authentication
class ObatainAuthTokenView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        contex = {}
        email = request.POST.get('email')
        password = request.POST.get('password')
        account = authenticate(email=email, password=password)
        if account:
            try:
                token = Token.objects.get(user=account)
            except Token.DoesNotExist:
                token = Token.objects.create(user=account)
            contex['response'] = "Successfully authenticated"
            contex['id'] = account.id
            contex['email'] = email
            contex['access_token'] = token.key
        else:
            contex['response'] = 'Error'
            contex['error_message'] = "Invalid credentials"

        return Response(contex)


@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):
    data = {}
    reqBody = request.data
    email1 = reqBody['email']
    password = reqBody['password']
    try:
        account = Account.objects.get(email=email1)
    except Account.DoesNotExist as e:
        return Response({"message": 'The account with the email does not exist.'})

    token = Token.objects.get_or_create(user=account)[0].key
    if not check_password(password, account.password):
        return Response({"message": "Incorrect signin credentials"})

    if account:
        if account.auth_provider != 'email':
            raise AuthenticationFailed(detail='Please login using ' + account.auth_provider)
            # return Response({"message": "Incorrect signin credentials"})
        else:
            if account.is_active:
                login(request, account)
                data["message"] = "user logged in"
                data["email_address"] = account.email
                Res = {"data": data, "token": token}

                return Response(Res)

            else:
                return Response({"message": f'Account not active'}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({"message": f'Account doesnt exist'})


# user login with OAuth2 authentiation
@api_view(['POST'])
def user_login(request):
    """
    user_login method define to check current user is authorised or not
    :param request:
    :return:
    """

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                print(">>>>>>>>>>>>>>>>>>", user.is_active)
                login(request, user)
                token = ''
                time_threshold = datetime.now()
                token_obj = AccessToken.objects.filter(user=user, expires__gt=time_threshold)
                contex = {}
                if token_obj:
                    token_obj = token_obj[0]
                    token = token_obj.token
                    contex['id'] = user.id
                    contex['username'] = username
                    contex['access_token'] = token
                else:
                    if not Application.objects.filter(user=1).exists():
                        Application.objects.create(user_id=6, authorization_grant_type='cre', client_type='confidential')
                    app_obj = Application.objects.filter(user=6)
                    if app_obj:
                        app_obj = app_obj[0]
                        print(">>>>>>>>>>>>>", app_obj)
                        client_id = app_obj.client_id
                        client_secret = app_obj.client_secret
                        url = 'http://' + request.get_host() + '/o/token/'
                        data_dict = {"grant_type": "password", "username": username, "password": password,
                                     "client_id": client_id, "client_secret": client_secret}
                        print(">>>>>>>data_dict>>>>>>", data_dict)
                        aa = requests.post(url, data=data_dict)
                        print(">>>>>>>>>>>", request.get_host())
                        data = aa.json()
                        print(">>>>>>>data>>>>", data)
                        token = data.get('access_token', '')
                    print(">>>>>>token>>>>>>", token)
                    contex['id'] = user.id
                    contex['username'] = username
                    contex['access_token'] = token
                return Response(contex)
            else:
                error_msg = "your account was inactive."
                return Response({'error': error_msg}, status=status.HTTP_408_REQUEST_TIMEOUT)
            return Response({'eror': 'error occured'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            error_msg = "wrong username or password, please try again with correct credentials"
            return Response({"error": error_msg}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({'eror': 'error occured'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def logoutUser(request):
    if logout(request):
        logout(request)
    return Response('User Logged out successfully')


class RefreshToken(APIView):
    def post(self, request):
        data = request.data
        print(data)
        user_id = data['user_id']
        client_id = data['client_id']
        client_secret = data['client_secret']
        token_obj = RefreshToken.objects.filter(user=user_id).order_by('-id')
        refresh_token = ''
        if token_obj:
            token_obj = token_obj[0]
            refresh_token = token_obj.token
            url = 'http://' + request.get_host() + '/o/token/'
            data_dict = {"grant_type": "refresh_token", "client_id": client_id, "client_secret": client_secret,
                         "refresh_token": refresh_token}
            print(">>>>>>>data_dict>>>>>>", data_dict)
            aa = requests.post(url, data=data_dict)
            print(">>>>>>>>>>>", request.get_host())
            data = aa.json()
            return Response(data, status=status.HTTP_201_CREATED)


class UserRegister(CsrfExemptMixin, OAuthLibMixin, APIView):
    permission_classes = (permissions.IsAuthenticated,)
    server_class = oauth2_settings.OAUTH2_SERVER_CLASS
    validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
    oauthlib_backend_class = oauth2_settings.OAUTH2_BACKEND_CLASS

    def post(self, request):
        if request.auth is None:
            data = request.data
            data = data.dict()
            serializer = RegisterSerializer(data=data)
            if serializer.is_valid():
                try:
                    with transaction.atomic():
                        user = serializer.save()
                        url, headers, body, token_status = self.create_token_response(request)
                        if token_status != 200:
                            raise Exception(json.loads(body).get("error_description", ""))
                        return Response(json.loads(body), status=token_status)
                except Exception as e:
                    return Response(data={"error": e.message}, status=status.HTTP_400_BAD_REQUEST)
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_403_FORBIDDEN)


class TokenView(APIView, CsrfExemptMixin, OAuthLibMixin):
    permission_classes = (permissions.IsAuthenticated,)

    server_class = oauth2_settings.OAUTH2_SERVER_CLASS
    validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
    oauthlib_backend_class = oauth2_settings.OAUTH2_BACKEND_CLASS

    def post(self, request):
        username = request.POST.get('username')
        serializer = RegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            AccessToken.objects.create(user=account.email)
        try:
            if username is None:
                raise Account.DoesNotExist
            AccessToken.objects.filter(user=Account.objects.get(username=username),
                                       application=Application.objects.get(name="oposh")).delete()
        except Account.DoesNotExist as e:
            print(e)
            return Response({'error': "no user found in the database"}, status=400)

        url, headers, body, status = self.create_token_response(request)
        return Response(body, status=status, headers=headers)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, ])
def CloseUserAccount(request):
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
