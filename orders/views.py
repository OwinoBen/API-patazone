import random

import requests
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from orders.models import PtzOrders, PtzCart
from orders.serializers import OrderSerializer, CartSerializer


@api_view(['POST', ])
@permission_classes([IsAuthenticated])
def placeOrder(request):
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
                serializer = OrderSerializer(data=response_data)
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
                        serializers = CartSerializer(data=cart_response)

                        if serializers.is_valid():
                            serializers.save()
                        else:
                            print(serializer.errors)
                            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    sendSMS(phone, order_id)
                    return Response({"order_id": order_id, "message": "Order placed successfully"},
                                    status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            elif response['payment_mode'] == 'Mpesa Express':
                mpesaPayment(order_id)
                pass
            elif response['payment_mode'] == 'Card payment':
                cardPayment(order_id)
                pass
            elif response['payment_mode'] == 'Pay with paypal':
                pass
            else:
                pass
        else:
            if response['payment_mode'] == 'Lipalater plan':
                lipaLaterPlan(order_id)
                pass
            elif response['payment_mode'] == 'Equity plan':
                equityPlan(order_id)
                pass
            elif response['payment_mode'] == 'Angaza Plan':
                pass
            else:
                pass

@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def getUserOrders(request):
    userID = request.user.id
    try:
        orders = PtzOrders.objects.filter(user_id=userID)
        for order in orders:
            order_details = PtzCart.objects.filter(order_id=order.order_id)
            serializers = CartSerializer(order_details, many=True)
    except PtzOrders.DoesNotExist:
        return Response({"success": False, "message": "Order not found"})
    if request.method == 'GET':
        serializer = OrderSerializer(orders, many=True)
        return Response({"order":serializer.data, "order_details": serializers.data}, status=status.HTTP_200_OK)


def cash_on_delivery_payment(response, order_id):
    pass


def mpesaPayment(order_id):
    pass


def cardPayment(order_id):
    pass


def paypalPayment(order_id):
    pass


def lipaLaterPlan(order_id):
    pass


def equityPlan(order_id):
    pass


def sendSMS(phone, orderID):
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
