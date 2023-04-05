from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, api_view
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from products.models import PtzProducts, PtzMultipleimgs, \
    PtzMainslidersettings, PtzBrands
from products.serializers import ProductSerializer, \
    productGallerySerializer, BannerSliderSerializer, BrandSeializer


@api_view(['GET', ])
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


class ApiProductsView(ListAPIView):
    queryset = PtzProducts.objects.filter(is_varified='yes', product_qty__gte=1).order_by("?")
    serializer_class = ProductSerializer
    authentication_classes = (TokenAuthentication,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('^product_title', '^discount_price', '^product_tags')


class getProductsByCategoryID(ListAPIView):
    serializer_class = ProductSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('product_title', 'selling_price', 'discount_price', 'product_tags', 'product_sku')

    def get_queryset(self):
        return PtzProducts.objects.filter(category_id=self.kwargs['category_id'], is_varified='yes',
                                          product_qty__gte=1).order_by("?")


class getSubCategoryProducts(ListAPIView):
    serializer_class = ProductSerializer
    authentication_classes = (TokenAuthentication,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('product_title', 'selling_price', 'discount_price', 'product_tags', 'product_sku')

    def get_queryset(self):
        return PtzProducts.objects.filter(subcategory_id=self.kwargs['subcateId'], product_qty__gte=1,
                                          is_varified="yes").order_by("?")


class getSub_subCategoryProducts(ListAPIView):
    serializer_class = ProductSerializer
    authentication_classes = (TokenAuthentication,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('product_title', 'selling_price', 'discount_price', 'product_tags', 'product_sku')

    def get_queryset(self):
        return PtzProducts.objects.filter(sub_subcategory_id=self.kwargs['subsubcateId'], product_qty__gte=1,
                                          is_varified="yes").order_by("?")


class getOfferProducts(ListAPIView):
    queryset = PtzProducts.objects.filter(special_offer=1, is_varified='yes', product_qty__gte=1).order_by('?')
    serializer_class = ProductSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('product_title', 'selling_price', 'discount_price', 'product_tags', 'product_sku')


class getFlashProducts(ListAPIView):
    queryset = PtzProducts.objects.filter(featured='', is_varified='yes', product_qty__gte=1).order_by("?")
    serializer_class = ProductSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('product_title', 'selling_price', 'discount_price', 'product_tags', 'product_sku')


class getRecommendedProducts(ListAPIView):
    serializer_class = ProductSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('product_title', 'selling_price', 'discount_price', 'product_tags', 'product_sku')

    def get_queryset(self):
        return PtzProducts.objects.filter(is_recomended=1, is_varified='yes', product_qty__gte=1).order_by("?")


class getRelatedProducts(ListAPIView):
    serializer_class = ProductSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('product_title', 'selling_price', 'discount_price', 'product_tags', 'product_sku')

    def get_queryset(self):
        return PtzProducts.objects.filter(subcategory_id=self.kwargs['subcategory_id'], is_varified='yes',
                                          product_qty__gte=1).order_by("?")


@api_view(['GET'])
@permission_classes([AllowAny, ])
def getProductGallery(request, product_id):
    try:
        gallery = PtzMultipleimgs.objects.filter(product_id=product_id)
    except PtzMultipleimgs.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = productGallerySerializer(gallery, many=True)
        return Response({"results": serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def getBannerSliders(request):
    paginator = PageNumberPagination()
    paginator.page_size = 10
    try:
        banner = PtzMainslidersettings.objects.filter(main_slider=1, is_active=1, soft_delete=0).order_by("?")
        page_results = paginator.paginate_queryset(banner, request)
    except PtzMainslidersettings.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = BannerSliderSerializer(page_results, many=True)
        return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def getBrands(request):
    paginator = PageNumberPagination()
    paginator.page_size = 10
    try:
        brands = PtzBrands.objects.filter(is_major=1, soft_delete=0).order_by("?")
        page_results = paginator.paginate_queryset(brands, request)
    except PtzMainslidersettings.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = BrandSeializer(page_results, many=True)
        return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def getSingleProductDetails(request, slug):
    paginator = PageNumberPagination()
    paginator.page_size = 10
    try:
        products = PtzProducts.objects.filter(id=slug)
        page_results = paginator.paginate_queryset(products, request)
    except PtzProducts.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ProductSerializer(products, many=True)
        return paginator.get_paginated_response(serializer.data)


@api_view(['GET'], )
@permission_classes([AllowAny])
def getProductsByBrands(request, brand_id):
    paginator = PageNumberPagination()
    paginator.page_size = 30
    if brand_id is not None:
        try:
            brand_products = PtzProducts.objects.filter(brand_id=brand_id, is_varified='yes',
                                                        product_qty__gte=1).order_by("?")
            results = paginator.paginate_queryset(brand_products, request)
        except PtzProducts.DoesNotExist:
            return Response({"message: No product found in the database."}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = ProductSerializer(results, many=True)
            return paginator.get_paginated_response(serializer.data)
