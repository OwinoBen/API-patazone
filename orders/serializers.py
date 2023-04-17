from rest_framework import serializers

from orders.models import PtzOrders, PtzCart, OrderItems, Orders


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


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = ['id', 'order', 'customer', 'product', 'ordered', 'quantity', 'updated_at', 'created_at']


class OrderSerializers(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Orders
        fields = [
            'id', 'order_id', 'coupon', 'amount_paid', 'total_amount',
            'status', 'ordered', 'received', 'refund_requested', 'refund_granted', 'shipping_total', 'active',
            'payment_mode', 'user_type', 'items', 'created_at', 'updated_at', 'soft_delete'
        ]

    def create(self, validated_data):
        print(validated_data)
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            print(user)
        order_items = validated_data.pop('items')
        order = Orders.objects.create(user=user, **validated_data)

        for item in order_items:
            OrderItems.objects.create(
                order=order,
                customer=user,
                **item
            )
        return order


