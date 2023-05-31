import os

import requests
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def geocode_api(request, lat, lng):
    # lat, lng = 40.714224, -73.961452
    global results
    api_key = GOOGLE_API_KEY
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    # endpoint = f"{base_url}?address=RNG Plaza, Ronald Ngala Street, Nairobi&key={api_key}"
    endpoint = f"{base_url}?latlng={lat},{lng}&key={api_key}"
    # see how our endpoint includes our API key? Yes this is yet another reason to restrict the key
    r = requests.get(endpoint)
    if r.status_code not in range(200, 299):
        return None, None
    try:
        '''
        This try block incase any of our inputs are invalid. This is done instead
        of actually writing out handlers for all kinds of responses.
        '''
        results = r.json()['results'][0]
        lat = results['geometry']['location']['lat']
        lng = results['geometry']['location']['lng']
    except:
        pass
    return Response(results, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_google_auto_complete_search(request, search):
    global results
    api_key = GOOGLE_API_KEY
    base_url = "https://maps.googleapis.com/maps/api/place/autocomplete/json"
    endpoint = f"{base_url}?input={search}&key={api_key}"

    r = requests.get(endpoint)
    if r.status_code not in range(200, 299):
        return None, None

    else:
        try:
            # results = r.json()['predictions']
            results = r.json()
        except:
            pass
    return Response(results, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_google_place_details(request, placeID):
    global results
    api_key = GOOGLE_API_KEY
    base_url = "https://maps.googleapis.com/maps/api/place/details/json"
    endpoint = f"{base_url}?place_id={placeID}&key={api_key}"

    r = requests.get(endpoint)
    if r.status_code not in range(200, 299):
        return None, None

    else:
        try:
            # results = r.json()['predictions']
            results = r.json()
        except:
            pass
    return Response(results, status=status.HTTP_200_OK)
