from rest_framework import serializers

from .models import PtzCustomers, PtzAddress





class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = PtzAddress
        fields = ['user_id', 'firstname', 'lastname', 'phone', 'address', 'latitude', 'longitude', 'address_type',
                  'is_default', 'date_created']





class userAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = PtzAddress
        fields = '__all__'


