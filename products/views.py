# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from utils.messages.hundle_messages import successResponse, errorResponse

from products.models import Product, ProductImages
from products.serializers import ProductSerializer, ProductImageSerializer


class ProductsViewSet(ModelViewSet):
    queryset = Product.objects.all().order_by('-created_date', '-pk')
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ProductSerializer
    parser_classes = (MultiPartParser, FormParser)

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ('^product_title', '^discount_price', '^product_tags')
    ordering_fields = ['product_title']
    pagination_class = PageNumberPagination

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        response_data = successResponse(status_code=status.HTTP_200_OK,
                                        message_code="get_data", message={"data": data})
        return Response(data=response_data)

    def create(self, request, *args, **kwargs):
        """Create products and multiple images referenced to the product"""

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
            response_data = errorResponse(status_code=status.HTTP_403_FORBIDDEN, error_code="permission_denied",
                                          message="Permission to access the resource denied. Contact system admin.")

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
        Modify Product details
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        instance = self.get_object()
        if not instance:
            response_data = errorResponse(status_code=status.HTTP_400_BAD_REQUEST, error_code="not_found",
                                          message="Resource not found")
            return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance, many=isinstance(request.data, list), partial=True, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance, serializer.validated_data)
        data = successResponse(status_code=status.HTTP_200_OK,
                               message_code="update_success",
                               message=f"{instance} updated successfully")
        headers = self.get_success_headers(serializer.data)
        return Response(data=data, status=status.HTTP_200_OK, headers=headers)

    @action(
        detail=True,
        methods=['post', 'delete'],
        url_name='update-gallery',
        url_path=r'update_gallery/(?P<gallery_id>\w+)')
    def update_gallery(self, request, pk=None, gallery_id=None):
        """
        Upload both single and multiple product images with the given params(product_id and image) only authenticated
        users can perform this action, Deletes product images in the product gallery list
        :param request:
        :param pk:
        :param gallery_id:
        :return:
        """
        if request.method == 'POST':
            flag = 1
            response_message = []
            try:
                product = Product.objects.get(product_id=pk)
            except ProductImages.DoesNotExist:
                response_data = errorResponse(status_code=status.HTTP_404_NOT_FOUND, error_code="not found",
                                              message="Product with the given details not found")
                return Response(response_data, status=status.HTTP_404_NOT_FOUND)
            response = request.data
            response['product'] = product.product_id
            images = dict(response.lists())['img']

            for image in images:
                modified_data = modify_inputs_for_files(product.product_id, image)
                serializer = ProductImageSerializer(data=modified_data, )
                if serializer.is_valid():
                    serializer.save()
                else:
                    flag = 0
                    response_message.append(serializer.errors)

            if flag == 1:
                data = successResponse(status_code=status.HTTP_200_OK,
                                       message_code="upload_success",
                                       message=f" Image/s uploaded successfully")
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                response_data = errorResponse(status_code=status.HTTP_400_BAD_REQUEST, error_code="bad request",
                                              message=response_message)
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'DELETE':
            try:
                if gallery_id is not None and pk is not None:
                    product = ProductImages.objects.get(product=pk, id=gallery_id)
                    if product:
                        product.delete()
                        response_message = successResponse(status_code=status.HTTP_204_NO_CONTENT,
                                                           message_code="delete_success",
                                                           message=f"Image Deleted successfully")
                        return Response(data=response_message, status=status.HTTP_204_NO_CONTENT)
            except ProductImages.DoesNotExist:
                response_data = errorResponse(status_code=status.HTTP_404_NOT_FOUND, error_code="not found",
                                              message="Instance not found")
                return Response(response_data, status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_200_OK)


def modify_inputs_for_files(product_id, image):
    serializer_data = {'img': image, 'product': product_id}
    return serializer_data


class ApiProductsView(ListAPIView):
    """
        Returns a list of all **active** Products in the system.

        For more details on how Products are verified please [see here][ref].

        [ref]: https://example.com/activating-accounts
        """
    # queryset = PtzProducts.objects.filter(is_verified='yes', product_qty__gte=1).order_by("?")
    serializer_class = ProductSerializer
    authentication_classes = (TokenAuthentication,)
    pagination_class = PageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('^product_title', '^discount_price', '^product_tags')
