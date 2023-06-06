from django.utils.text import slugify
from rest_framework import serializers, status

from categories.models import Categories
from products.models import Product, ProductImages, Brands


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = ('id', 'product', 'img', 'date_created')


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(

        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False), write_only=True, )

    class Meta:
        model = Product
        fields = ("product_id", "product_title",
                  "vendor", "slug", "brand", "category", "subcategory",
                  "subsubcategory", "meta_title", "meta_keywords",
                  "meta_description", "product_sku", "product_qty",
                  "selling_price", "discount_price",
                  "variation", "barcode", "product_thumbnail",
                  "hot_deals", "featured",
                  "recommended", "short_description",
                  "product_specification", "long_description",
                  "is_verified",
                  "live", "same_day_deliver",
                  "next_day_delivery", "hyper_local_delivery",
                  "min_order_count",
                  "max_order_count", "return_days",
                  "out_of_stock_sell",
                  "created_date", "updated_date",
                  "images", "uploaded_images"
                  )
        read_only_fields = ['updated_date', 'created_date', 'product_id', 'slug']

    def create(self, validated_data):
        uploaded_images = validated_data.pop('uploaded_images')  # remove uploaded images field from the object
        slug = slugify(validated_data['product_title'])

        try:
            products = Product.objects.get(slug=slug)
            if products:
                raise serializers.ValidationError({'success': 0, "code": status.HTTP_400_BAD_REQUEST,
                                                   'message': 'The product with the title already exists'})
        except Product.DoesNotExist:
            # get the rest of the body fields and save them to the database
            product = Product.objects.create(**validated_data)

            for img in uploaded_images:
                ProductImages.objects.create(product=product, img=img)

            return product

    def update(self, instance, validated_data):
        global product_brand
        uploaded_images = validated_data.pop('uploaded_images')


        if validated_data['subcategory'] is not None or \
                validated_data['subsubcategory'] is not None or validated_data['brand'] is not None:
            product_category = validated_data.pop('category')
            product_subcategory = validated_data.pop('subcategory')
            product_subsubcategory = validated_data.pop('subsubcategory')
            product_brand = validated_data.pop('brand')
            category_instance = Categories.objects.get(id=str(product_category))
            brand_instance = Brands.objects.get(brand_id=str(product_brand))

        updated_fields = [k for k in validated_data]

        for k, v in validated_data.items():
            setattr(instance, k, v)

        instance.save(update_fields=updated_fields)

        """getting list of product gallery"""
        product_gallery = ProductImages.objects.filter(product=instance.product_id)

        product_images_id = []
        print(uploaded_images)
        for image in uploaded_images:
            if "id" in image.keys():
                if ProductImages.objects.filter(id=image[id]).exists():
                    product_image_instance = ProductImages.objects.get(id=image['id'])
                    product_instance = Product.objects.get(product_id=image.get('product'))
                    product_image_instance.product = product_instance
                    product_image_instance.img = image.get('img', product_image_instance.img)

                    product_image_instance.save()
                    product_images_id.append(product_image_instance.id)
                else:
                    continue
            else:
                product_instance = Product.objects.get(product_id=image['product'])
                new_item_instance = ProductImages.objects.create(
                    product=product_instance,
                    img=image['img'],
                )
                product_images_id.append(new_item_instance.id)
                for product_image_id in product_gallery:
                    if product_image_id not in product_images_id:
                        ProductImages.objects.filter(id=product_image_id).delete()

            return instance
