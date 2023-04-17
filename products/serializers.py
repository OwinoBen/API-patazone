from django.utils.text import slugify
from rest_framework import serializers, status
from rest_framework.response import Response

from products.models import PtzProducts, PtzMultipleimgs, PtzBrands, PtzMainslidersettings, Product, ProductImages


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


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ('id', 'product', 'img', 'date_created')


class ProductSerializers(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(

        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False), write_only=True, )

    class Meta:
        model = Product
        fields = ("product_id", "product_title", "shop_name", "slug", "brand", "category", "subcategory",
                  "subsubcategory", "product_tags", "product_sku", "product_qty", "selling_price", "discount_price",
                  "variation", "barcode", "product_thumbnail", "hot_deals", "featured",
                  "recommended", "short_description", "product_specification", "long_description", "is_verified",
                  "created_date", "updated_date", "images", "uploaded_images"
                  )
        read_only_fields = ['updated_date', 'created_date', 'product_id', 'slug']

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images')  # remove uploaded images field from the object
        slug = slugify(validated_data['product_title'])

        try:
            products = Product.objects.get(slug=slug)
            if products:
                # return Response()
                raise serializers.ValidationError({'success': 0, "code": status.HTTP_400_BAD_REQUEST,
                                                   'message': 'The product with the title already exists'})
        except Product.DoesNotExist:
            # get the rest of the body fields and save them to the database
            product = Product.objects.create(**validated_data)

            for img in uploaded_images:
                ProductImages.objects.create(product=product, img=img)

            return product


class BannerSliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PtzMainslidersettings
        fields = '__all__'


class BrandSeializer(serializers.ModelSerializer):
    class Meta:
        model = PtzBrands
        fields = "__all__"
