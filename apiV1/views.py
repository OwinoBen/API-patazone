import json
import stat
from datetime import datetime

import requests
from django.contrib.auth import authenticate, login
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from oauth2_provider.contrib.rest_framework import permissions
from oauth2_provider.models import AccessToken, Application, RefreshToken
from oauth2_provider.settings import oauth2_settings
from oauth2_provider.views.mixins import OAuthLibMixin
from braces.views import CsrfExemptMixin
from rest_framework import status, serializers
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView

from .models import PtzAccountUsers, PtzProducts, Account, PtzCategories, PtzSubcategories, PtzSubsubcategories, \
    PtzMultipleimgs

from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView

from .serializers import UserSerializer, ProductSerializer, RegistrationSerializer, AccountPropertiesSerializer, \
    RegisterSerializer, CategorySerializer, SubcategorySerializer, SubsubcategorySerializer, productGallerySerializer


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


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def viewProducts(request):
    try:
        products = PtzProducts.objects.all()
    except PtzProducts.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


@api_view(['PUT', ])
@permission_classes((IsAuthenticated,))
def updateProducts(request):
    try:
        products = PtzProducts.objects.get(id=31)
    except PtzProducts.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ProductSerializer(products, data=request.data)
        data = {}

        if serializer.is_valid():
            serializer.save()
            data["success"] = "Product updated successfully"
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def deleteProducts(request):
    try:
        products = PtzProducts.objects.get(id=56)
    except PtzProducts.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        operation = products.delete()
        data = {}
        if operation:
            data["success"] = "product was deleted successfully"
        else:
            data["failure"] = "delete operation failed"
        return Response(data=data)


@api_view(['POST', ])
def addProduct(request):
    pass


@api_view(['POST'])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'successfully registered new user'
            data['email'] = account.email
            data['username'] = account.username
            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)


class ApiProductsView(ListAPIView):
    queryset = PtzProducts.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('product_title', 'selling_price', 'discount_price', 'product_tags', 'product_sku')


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
            data['response'] = "Account successfullu updated"
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# user login with token authentication
class ObatainAuthTokenView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        contex = {}
        email = request.POST.get('username')
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
                        Application.objects.create(user_id=6, authorization_grant_type='cre',
                                                   client_type='confidential')
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getCategories(request):
    try:
        categories = PtzCategories.objects.all()
    except PtzCategories.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getSubcategories(request):
    try:
        subcategories = PtzSubcategories.objects.all()
    except PtzSubcategories.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = SubcategorySerializer(subcategories, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated], )
def getSingleSubcategoty(request, categoryid):
    try:
        subcate = PtzSubcategories.objects.filter(category_id=categoryid)
    except PtzSubcategories.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = SubcategorySerializer(subcate, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def getSubsubCategory(request):
    try:
        subsub = PtzSubsubcategories.objects.all()
    except PtzSubsubcategories.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = SubcategorySerializer(subsub, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated], )
def getSingleSubsubcategory(request, subcategoryid):
    try:
        subcate = PtzSubsubcategories.objects.filter(subcategory_id=subcategoryid)
    except PtzSubsubcategories.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = SubsubcategorySerializer(subcate, many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getSingleProductDetails(request, slug):
    try:
        products = PtzProducts.objects.filter(slug=slug)
    except PtzProducts.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class getProductsByCategoryID(ListAPIView):
    # queryset = PtzProducts.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('product_title', 'selling_price', 'discount_price', 'product_tags', 'product_sku')

    def get_queryset(self):
        return PtzProducts.objects.filter(category_id=self.kwargs['category_id'])


class getSubCategoryProducts(ListAPIView):
    serializer_class = ProductSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('product_title', 'selling_price', 'discount_price', 'product_tags', 'product_sku')

    def get_queryset(self):
        return PtzProducts.objects.filter(subcategory_id=self.kwargs['subcateId'])


class getOfferProducts(ListAPIView):
    queryset = PtzProducts.objects.filter(hot_deals=1)
    serializer_class = ProductSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('product_title', 'selling_price', 'discount_price', 'product_tags', 'product_sku')


class getFlashProducts(ListAPIView):
    serializer_class = ProductSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('product_title', 'selling_price', 'discount_price', 'product_tags', 'product_sku')

    def get_queryset(self):
        return PtzProducts.objects.filter(featured=1)


# @api_view(['GET'])
# def getFlashProducts(request, id):
#     print("flashProducts")
#     try:
#         flashProducts = PtzProducts.objects.filter(featured=1)
#         print("flashProducts")
#     except PtzProducts.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         serializer = ProductSerializer(flashProducts)
#         return Response(serializer.data)
#

@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def getProductGallery(request, product_id):
    try:
        gallery = PtzMultipleimgs.objects.all()
    except PtzMultipleimgs.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = productGallerySerializer(gallery, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
