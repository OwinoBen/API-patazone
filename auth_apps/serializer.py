from django.conf import settings
from rest_framework import serializers, exceptions, status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from utils.messages.hundle_messages import successResponse
from .models import Account, PtzAccountUsers


class RegistrationSerializers(serializers.ModelSerializer, TokenObtainPairSerializer):
    confirm_psd = serializers.CharField(style={input: 'password'}, write_only=True)

    class Meta:
        model = Account
        fields = ['id', 'email', 'firstname', 'lastname', 'phone', 'password', 'confirm_psd']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        """
        overrides the parent serializer class validate method
        :param attrs:
        :return:
        """
        if Account.objects.filter(email=attrs['email']).exists():
            raise exceptions.AuthenticationFailed('The user with the email provided exist', "user_exists", )
        else:
            password = attrs['password']
            password2 = attrs['confirm_psd']
            attrs.pop('confirm_psd')
            if password != password2:
                raise exceptions.AuthenticationFailed('Passwords must match.', "password_mismatch", )
            user = Account.objects.create_user(
                **attrs
            )
            user.set_password(password)
            user.save()
            token = super().validate(attrs)
            data = {
                "token": token,
                "expires_in": settings.SIMPLE_JWT.get('ACCESS_TOKEN_LIFETIME')
            }
            response_data = successResponse(status_code=status.HTTP_200_OK, message_code="authentication",
                                            message=data)
        return response_data


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={input: 'password'}, write_only=True)

    class Meta:
        model = Account
        fields = ['email', 'firstname', 'lastname', 'phone', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = Account(
            email=self.validated_data['email'],
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
        user.set_password(password)
        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PtzAccountUsers
        fields = ['first_name', 'last_name', 'phone', 'date_registered', 'is_vendor', 'date_updated']


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
