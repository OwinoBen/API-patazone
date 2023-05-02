from rest_framework import serializers

from orders.models import PtzOrders, PtzCart, OrderItems, Orders
from products.models import Product


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
        read_only_fields = ('order', 'customer',)


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
        user = None
        payment_mode = validated_data['payment_mode']
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        if payment_mode == 'Cash':
            order_items = validated_data.pop('items')
            order = Orders.objects.create(user=user, **validated_data)

            for item in order_items:
                OrderItems.objects.create(
                    order=order,
                    customer=user,
                    **item
                )
            return order

    def update(self, instance, validated_data):
        item_list = validated_data.pop('items')
        updated_field = [k for k in validated_data]
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save(update_fields=updated_field)

        """getting list of orderItems"""
        order_items = OrderItems.objects.filter(order=instance.id).values_list('id', flat=True)
        items_id = []
        for item in item_list:

            if "id" in item.keys():
                if OrderItems.objects.filter(id=item['id']).exists():
                    item_instance = OrderItems.objects.get(id=item['id'])
                    product_instance = Product.objects.get(product_id=item['product'])

                    item_instance.product = product_instance

                    item_instance.quantity = item.get('quantity', item_instance.quantity)
                    item_instance.ordered = item.get('ordered', item_instance.ordered)

                    item_instance.save()
                    items_id.append(item_instance.id)
                else:
                    continue
            else:
                product_instance = Product.objects.get(product_id=item['product'])
                new_item_instance = OrderItems.objects.create(order=instance, customer=self.context['request'].user,
                                                              product=product_instance,
                                                              quantity=item['quantity'],
                                                              ordered=item['ordered']
                                                              )
                items_id.append(new_item_instance.id)
                for item_id in order_items:
                    if item_id not in items_id:
                        OrderItems.objects.filter(id=item_id).delete()

        return instance
