import random
from rest_framework import serializers

from orders.models import OrderItems, Orders
from products.models import Product


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = ['id', 'order', 'customer', 'product', 'ordered', 'quantity', 'updated_at', 'created_at']
        read_only_fields = ('order', 'customer',)


class OrderSerializer(serializers.ModelSerializer):
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
            orderId = 'PTZORD' + str(random.randint(1, 1000000))
            order_id = orderId
            order = Orders.objects.create(user=user, order_id=order_id, **validated_data)

            for item in order_items:
                OrderItems.objects.create(
                    order=order,
                    customer=user,
                    **item
                )
            return order

    def update(self, instance, validated_data):

        items = validated_data.pop('items')
        updated_field = [k for k in validated_data]
        for k, v in validated_data.items():
            setattr(instance, k, v)
        instance.save(update_fields=updated_field)

        """getting list of orderItems"""
        order_items = OrderItems.objects.filter(order=instance.id).values_list('id', flat=True)
        items_id = []
        for item in items:

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
