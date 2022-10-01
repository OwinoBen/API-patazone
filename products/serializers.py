from rest_framework import serializers

from products.models import PtzProducts, PtzMultipleimgs, PtzBrands, PtzMainslidersettings


class productGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = PtzMultipleimgs
        fields = '__all__'
        depth = 2


class ProductSerializer(serializers.ModelSerializer):
    # product_gallery = productGallerySerializer(many=True)

    class Meta:
        model = PtzProducts
        fields = '__all__'


class BannerSliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PtzMainslidersettings
        fields = '__all__'


class BrandSeializer(serializers.ModelSerializer):
    class Meta:
        model = PtzBrands
        fields = "__all__"