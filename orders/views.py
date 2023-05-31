import random

import requests
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from orders.models import Orders
from orders.serializers import OrderSerializers
from utils.messages.hundle_messages import successResponse, errorResponse


@api_view(['POST', ])
@permission_classes([IsAuthenticated])
def place_order(request):
    response = request.data
    order_number = random.randint(0, 100000)
    order_id = 'PTZORD' + str(order_number)
    code = str(+254)

    response_data = {
        "order_id": order_id,
        "user_id": response['user_id'],
        "payment_id": response['payment_id'],
        "amount_paid": response['amount_paid'],
        "is_paid": response['is_paid'],
        "payment_mode": response['payment_mode'],
        "order_status": response['order_status'],
        "user_type": response['user_type']
    }

    if request.method == 'POST':
        response_phone = response['phone']
        phone = code + response_phone[-9:]

        if response['payment_option'] == 'Direct payment':
            if response['payment_mode'] == 'Pay on delivery':
                serializer = OrderSerializers(data=response_data)
                if serializer.is_valid():
                    serializer.save()
                    cartItems = response['cart']
                    cart_response = {}
                    for cart in cartItems:
                        if cart['discountPrice'] is not None:
                            product_price = cart['discountPrice']
                        else:
                            product_price = cart['sellingPrice']
                        cart_response = {
                            "user_id": response['user_id'],
                            "product": cart['id'],
                            "order": order_id,
                            "product_name": cart['productTitle'],
                            "product_qty": cart['quantity'],
                            "product_price": product_price,
                            "ordered": 1,
                            "product_image": cart['productThumbnail'],
                            "product_sku": cart['product']['product_sku'],
                            "product_slug": cart['product']['slug']
                        }
                        serializers = cart_response

                        if serializers.is_valid():
                            serializers.save()
                        else:
                            return Response({"message": serializers.errors}, status=status.HTTP_400_BAD_REQUEST)
                    send_sms(phone, order_id)
                    return Response({"order_id": order_id, "message": "Order placed successfully"},
                                    status=status.HTTP_200_OK)
                return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            elif response['payment_mode'] == 'Mpesa Express':
                mpesa_payment(order_id)
                return Response({"message": "Payment method not available now, you can use cash option instead"},
                                status=status.HTTP_400_BAD_REQUEST)
            elif response['payment_mode'] == 'Card payment':
                card_payment(order_id)
                return Response({"message": "Payment method not available now, you can use cash option instead"},
                                status=status.HTTP_400_BAD_REQUEST)
            elif response['payment_mode'] == 'Pay with paypal':
                return Response({"message": "Payment method not available now, you can use cash option instead"},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Payment method not available now, you can use cash option instead"},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            if response['payment_mode'] == 'Lipalater plan':
                lipa_later_plan(order_id)
                return Response({"message": "Payment method not available now, you can use cash option instead"},
                                status=status.HTTP_400_BAD_REQUEST)
            elif response['payment_mode'] == 'Equity plan':
                equity_plan(order_id)
                return Response({"message": "Payment method not available now, you can use cash option instead"},
                                status=status.HTTP_400_BAD_REQUEST)
            elif response['payment_mode'] == 'Angaza Plan':
                return Response({"message": "Payment method not available now, you can use cash option instead"},
                                status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Payment method not available now, you can use cash option instead"},
                                status=status.HTTP_400_BAD_REQUEST)


class OrderView(ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrderSerializers
    pagination_class = PageNumberPagination
    # parser_classes = (MultiPartParser, FormParser)

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ('^order_id', '^amount_paid', '^status', 'received')
    ordering_fields = ['order_id']

    def retrieve(self, request, *args, **kwargs):
        """
        Fetch order by the orderID
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        response_data = successResponse(status_code=status.HTTP_200_OK, message_code="get_data", message={"data": data})
        return Response(data=response_data)

    def update(self, request, *args, **kwargs):
        """
            Modify orders details
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        instance = self.get_object()
        if not instance:
            response_data = errorResponse(status_code=status.HTTP_400_BAD_REQUEST, error_code="not_found", message="Resource not found")
            return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance, many=isinstance(request.data, list), partial=True, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance, request.data)
        data = successResponse(status_code=status.HTTP_200_OK,
                               message_code="update_success",
                               message=f"{instance} updated successfully")
        headers = self.get_success_headers(serializer.data)
        return Response(data=data, status=status.HTTP_200_OK, headers=headers)

    def destroy(self, request, *args, **kwargs):
        """
        Delete order from the database
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        if not (not request.user.is_superuser and not request.user.is_admin):
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






def cash_on_delivery_payment(response, order_id):
    pass


def mpesa_payment(order_id):
    pass


def card_payment(order_id):
    pass


def paypal_payment(order_id):
    pass


def lipa_later_plan(order_id):
    pass


def equity_plan(order_id):
    pass


def send_sms(phone, orderID):
    url = 'https://vas.teleskytech.com/api/sendsms'
    message = "Dear Customer, \nthank you for your order. \nWe have received your order " + orderID + " and will contact you as soon as your package is shipped. \n. Regards, \nPatazone Team."
    data = {
        "username": "patazoneinvestment",
        "api": "f157ddfab568",
        "phone": phone,
        "from": "Patazone",
        "message": message
    }
    headers = {
        'Accept: application/json',
        'Content-Type: application/json'
    }

    response = requests.post(url, json=data)
    return response


@api_view(['POST', ])
def is_phone_number_valid(request, phone):
    print(phone[-9:])
    return Response({"matched": True})



