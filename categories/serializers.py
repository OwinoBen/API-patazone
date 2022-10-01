from rest_framework import serializers

from apiV1.models import PtzCategories, PtzSubcategories, PtzSubsubcategories


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PtzCategories
        fields = ['id', 'category_name', 'category_thumbnail', 'category_image', 'date_created']


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PtzSubcategories
        fields = ['id', 'category_id', 'subcategory_name', 'date_created', 'date_updated']


class SubsubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PtzSubsubcategories
        fields = ['id', 'category_id', 'subcategory_id', 'sub_subcategory_name','subsub_category_image', 'date_created', 'date_updated']