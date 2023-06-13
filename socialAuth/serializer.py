from rest_framework import serializers

from socialAuth.register_social_user import register_social_user
from socialAuth.social_helper.Facebook_helper import Facebook
from socialAuth.social_helper.Google_helper import Google


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        userdata = Google.validate(auth_token)
        try:
            userdata['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please try again.'
            )
        # if userdata['aud'] != os.environ.get('GOOGLE_CLIENT_ID'):
        #     raise AuthenticationFailed('oops, who are you')
        # user_id = userdata['sub']
        email = userdata['email']
        firstname = userdata['given_name']
        lastname = userdata['family_name']
        provider = 'google'

        return register_social_user(
            provider=provider,
            email=email,
            firstname=firstname,
            lastname=lastname
        )


class FacebookAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        try:
            user_data = Facebook.validate(auth_token)
        except Exception:
            raise serializers.ValidationError('The token is invalid or expired. Please login again')

        # user_id = user_data['id']
        email = user_data['email']
        firstname = user_data['first_name']
        lastname = user_data['last_name']
        provider = 'facebook'
        return register_social_user(email=email, firstname=firstname, lastname=lastname,
                                    provider=provider)
