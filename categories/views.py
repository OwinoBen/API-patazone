from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apiV1.models import PtzSubsubcategories, PtzSubcategories, PtzCategories
from categories.serializers import SubsubcategorySerializer, SubcategorySerializer, CategorySerializer


@api_view(['GET'])
def getCategories(request):
    paginator = PageNumberPagination()
    paginator.page_size = 10
    try:
        categories = PtzCategories.objects.filter(is_topcategory=1)
        page_results = paginator.paginate_queryset(categories, request)
    except PtzCategories.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = CategorySerializer(page_results, many=True)
        return paginator.get_paginated_response(serializer.data)


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
def getSingleSubcategory(request, categoryid):
    paginator = PageNumberPagination()
    paginator.page_size = 10
    try:
        subcate = PtzSubcategories.objects.filter(category_id=categoryid)
        page_results = paginator.paginate_queryset(subcate, request)
    except PtzSubcategories.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = SubcategorySerializer(page_results, many=True)
        return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
def getSubsubCategory(request):
    try:
        subsub = PtzSubsubcategories.objects.all()
    except PtzSubsubcategories.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = SubcategorySerializer(subsub, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getSingleSubsubcategory(request, categoryid):
    paginator = PageNumberPagination()
    paginator.page_size = 10
    try:
        subcate = PtzSubsubcategories.objects.filter(category_id=categoryid).order_by("?")
        page_results = paginator.paginate_queryset(subcate, request)
    except PtzSubsubcategories.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = SubsubcategorySerializer(page_results, many=True)
        return paginator.get_paginated_response(serializer.data)
