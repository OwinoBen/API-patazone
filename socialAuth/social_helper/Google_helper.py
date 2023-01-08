from google.auth.transport import requests
from google.oauth2 import id_token, service_account, credentials


class Google:
    @staticmethod
    def validate(auth_token):
        try:
            idinfo = id_token.verify_oauth2_token(
                auth_token, requests.Request())
            # idinfo = id_token.verify_firebase_token(
            #     auth_token, requests.Request())
            if 'accounts.google.com' in idinfo['iss']:  # iss google issuer
                return idinfo
        except:
            return "The token is either invalid or expired"
