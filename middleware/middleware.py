class CustomHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response['Developer'] = "Opondo Benson, <Senior software developer Patazone>"

        return response
