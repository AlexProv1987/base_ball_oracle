from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from base_ball_oracle.settings import GOOGLE_MAPS_API_KEY, PROJECT_SPORT
from base_ball_oracle.globals import GlobalLevels, ConvertValue
import googlemaps
from base_ball_oracle.global_mixins import ValidateParamsMixIn
from .serializers import SearchedLeaugesSerializer
# Create your views here.
class LeagueFinder(APIView, GlobalLevels,ValidateParamsMixIn):

    google_maps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
    accepted_params = {'age':int.__name__, 'zip':int.__name__}

    def get(self,request,*args,**kwargs):
        if self.validate_keys(request):
            avail_places = self.get_avail_options(request)
            return Response(data={'totalplaces':len(avail_places), 'places':avail_places}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def get_avail_options(self,request):
        places = self.google_maps.places_nearby(
        keyword=self.create_query_string(request.query_params['age']), 
        location=self.get_person_location(request.query_params['zip']),
        radius=ConvertValue.convert(25,1609),
        language='en-US',
        )
        self.capture_request(request.query_params['zip'],len(places['results']))
        place_ids = self.consolidate_response(places)
        detailed_places = self.return_place_details(place_ids)
        return detailed_places
    
    def get_person_location(self,zip):
        get_location = self.google_maps.geocode(zip)
        location = f"{get_location[0]['geometry']['location']['lat']},{get_location[0]['geometry']['location']['lng']}"
        return location

    def consolidate_response(self,locresponse):
        avail_list = []
        i = 0
        for place in locresponse['results']:
            if i < 3:
                avail_list.append(place['place_id'])
            else:
                return avail_list
            i+=1
        return avail_list
    
    def return_place_details(self, places):
        place_details = []
        for place in places:
            phone_num = 'Not Available'
            p_detail = self.google_maps.place(place_id=place)
            if 'formatted_phone_number' in p_detail['result']:
                phone_num = p_detail['result']['formatted_phone_number']
            place_details.append({'name':p_detail['result']['name'],'address':p_detail['result']['formatted_address'],'phone': phone_num})
        return place_details

    def create_query_string(self, age_req):
        qs = ''
        level = self.get_player_level(int(age_req))
        if level is None:
            qs = f'{PROJECT_SPORT} league'
        if level is GlobalLevels.T_BALL:
            qs = f'{level} league'
        else:
            qs = f'{level} {PROJECT_SPORT} league'
        return qs
    

    def capture_request(self,zip,places_cnt):
        serializer = SearchedLeaugesSerializer(data={'total_found':places_cnt, 
                                                     'zip_searched':zip})
        serializer.is_valid(raise_exception=True)
        serializer.save()
