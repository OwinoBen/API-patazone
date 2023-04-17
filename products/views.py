from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes, api_view
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from utils.messages.hundle_messages import successResponse, errorResponse

from products.models import PtzProducts, PtzMultipleimgs, \
    PtzMainslidersettings, PtzBrands, Product
from products.serializers import ProductSerializer, \
    productGallerySerializer, BannerSliderSerializer, BrandSeializer, ProductSerializers


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


class ProductsViewSet(ModelViewSet):
    queryset = Product.objects.all().order_by('-created_date', '-pk')
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ProductSerializers
    parser_classes = (MultiPartParser, FormParser)

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ('^product_title', '^discount_price', '^product_tags')
    ordering_fields = ['product_title']
    pagination_class = PageNumberPagination

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        response_data = successResponse(status_code=status.HTTP_200_OK, message_code="get_data", message={"data": data})
        return Response(data=response_data)

    def create(self, request, *args, **kwargs):
        """Create products and multiple images referenced to the product"""

        # serializers = self.serializer_class(data=request.data)

        if request.user.is_admin or request.user.is_staff or request.user.is_vendor or request.user.is_superuser:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.create(serializer.validated_data)
            headers = self.get_success_headers(serializer.validated_data)
            response_data = successResponse(status_code=status.HTTP_201_CREATED,
                                            message_code="upload_success",
                                            message={
                                                "message": [f"{serializer.data['product_title']} uploaded "
                                                            f"successfully."]},
                                            )

            return Response(data=response_data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            response_data = errorResponse(status_code=status.HTTP_403_FORBIDDEN, error_code="permission_denied", message="Permission to access the resource denied. Contact system admin.")

            return Response(data=response_data, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        """
        deletes product from the database with the given product id
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        if request.user.is_superuser or request.user.is_admin:
            instance = self.get_object()

            self.perform_destroy(instance)
            response_data = successResponse(status_code=status.HTTP_204_NO_CONTENT,
                                            message_code="delete_success",
                                            message=f"{instance} deleted successfully.")

            return Response(data=response_data, status=status.HTTP_204_NO_CONTENT)
        else:
            response_data = errorResponse(status_code=status.HTTP_403_FORBIDDEN, error_code="permission_denied",
                                          message="You have no permission to delete the resource. Contact "
                                                  "system admin to grant permission.")

            return Response(data=response_data, status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        """
        modelSetView update method
        performing product update operations and patch operations
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        if request.user.is_admin or request.user.is_staff or request.user.is_vendor or request.user.is_superuser:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            data = successResponse(status_code=status.HTTP_200_OK,
                                   message_code="update_success",
                                   message=f"{instance} updated successfully")
            headers = self.get_success_headers(serializer.data)
            return Response(data=data, status=status.HTTP_200_OK, headers=headers)
        else:
            response_data = errorResponse(status_code=status.HTTP_403_FORBIDDEN, error_code="permission_denied",
                                          message="You have no permission to update the resource.Contact "
                                                  "system admin to grant permission.")

            return Response(data=response_data, status=status.HTTP_403_FORBIDDEN)


class ApiProductsView(ListAPIView):
    """
        Returns a list of all **active** Products in the system.

        For more details on how Products are verified please [see here][ref].

        [ref]: http://example.com/activating-accounts
        """
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
