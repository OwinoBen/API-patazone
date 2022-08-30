from rest_framework import serializers

from .models import PtzAccountUsers, PtzProducts, PtzCustomers, Account, PtzCategories, PtzSubcategories, \
    PtzSubsubcategories, PtzAddress, PtzMultipleimgs, PtzMainslidersettings, PtzBrands


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PtzAccountUsers
        fields = ['first_name', 'last_name', 'phone', 'date_registered', 'is_vendor', 'date_updated']


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


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={input: 'password'}, write_only=True)

    class Meta:
        model = Account
        fields = ['email', 'firstname', 'lastname', 'phone', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        account = Account(
            email=self.validated_data['email'],
            # username=self.validated_data['username'],
            firstname=self.validated_data['firstname'],
            lastname=self.validated_data['lastname'],
            phone=self.validated_data['phone'],
        )

        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if Account.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'email error': 'The user with the email provided exist'})

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        account.set_password(password)
        account.save()
        return account


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = PtzAddress
        fields = ['user_id', 'firstname', 'lastname', 'phone', 'address', 'latitude', 'longitude', 'address_type',
                  'is_default', 'date_created']


class AccountPropertiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'email', 'firstname', 'lastname', 'phone']


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={input: 'password'}, write_only=True)

    class Meta:
        model = Account
        fields = ['email', 'firstname', 'lastname', 'phone', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        try:
            user = Account.objects.filter(phone=data.get('phone'))
            if len(user) > 0:
                raise serializers.ValidationError("Phone number already exists")
        except Account.DoesNotExist:
            pass

        if not data.get('password') or not data.get('password2'):
            raise serializers.ValidationError("Password field is required")
        if data.get('password') != data.get('password2'):
            raise serializers.ValidationError("Password mismatch")
        return data


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
        fields = ['id', 'category_id', 'subcategory_id', 'sub_subcategory_name', 'date_created', 'date_updated']


class userAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = PtzAddress
        fields = '__all__'


class BannerSliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PtzMainslidersettings
        fields = '__all__'


class BrandSeializer(serializers.ModelSerializer):
    class Meta:
        model = PtzBrands
        fields = "__all__"
