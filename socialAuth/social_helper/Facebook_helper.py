import facebook


class Facebook:
    @staticmethod
    def validate(auth_token):
        try:
            graph = facebook.GraphAPI(access_token=auth_token)
            profile = graph.request('/me?fields=first_name,last_name,email')
            return profile
        except:
            return "The token is invalid or has expired"
