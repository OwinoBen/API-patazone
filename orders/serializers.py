from rest_framework import serializers

from orders.models import PtzOrders, PtzCart


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PtzOrders
        fields = ['order_id', 'user_id', 'payment_id', 'amount_paid', 'is_paid', 'payment_mode', 'order_status',
                  'user_type'
                  ]


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = PtzCart
        fields = ['user_id', 'product', 'order', 'product_name', 'product_qty', 'product_price', 'ordered',
                  'product_image', 'product_sku', 'product_slug'
                  ]
