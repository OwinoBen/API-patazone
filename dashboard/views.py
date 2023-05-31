from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView
import datetime
from django.utils import timezone

from orders.models import Orders, OrderManagementQuerySet
from orders.serializers import OrderSerializers


class DashboardView(ListAPIView):
    serializer_class = OrderSerializers

    queryset = Orders.objects.get_orders_by_weeks_range(2, 8)

