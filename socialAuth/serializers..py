import os

import google
from rest_framework import serializers

from socialAuth.social_helper.Google_helper import Google


class GoogleSocialAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        # userdata = google.Google.validate(auth_token)
        userdata = Google.validate(auth_token)
        try:
            userdata['sub']
        except:
            raise serializers.ValidationError(
                'The token is invalid or expired. Please login again'
            )
        if userdata['aud'] !=os.environ.get('GOOGLE_CLIENT_ID'):
            raise AuthenticationFailed('oops, who are you')
        user_id =userdata['sub']
        email = userdata['email']
        name = userdata['name']
        provider = 'google'

        return register_social_user(
            provider=provider,
            user_id=user_id,
            email=email,
            name=name
        )
