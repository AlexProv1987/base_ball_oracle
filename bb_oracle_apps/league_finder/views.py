from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from base_ball_oracle.settings import GOOGLE_MAPS_API_KEY, PROJECT_SPORT
from base_ball_oracle.globals import GlobalLevels, ConvertValue
import googlemaps
# Create your views here.
class LeagueFinder(APIView, GlobalLevels):

    google_maps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

    def get(self,request,*args,**kwargs):
        avail_places = self.get_avail_options(request)
        return Response(data={'totalplaces':len(avail_places), 'places':avail_places}, status=status.HTTP_200_OK)
    
    def get_avail_options(self,request):
        places = self.google_maps.places_nearby(
        keyword=self.create_query_string(request.query_params['age']), 
        location=self.get_person_location(request),
        radius=ConvertValue.convert(25,1609),
        language='en-US',
        )
        shrunk = self.consolidate_response(places)
        return shrunk
    
    def get_person_location(self,request):
        get_location = self.google_maps.geocode({request.query_params['zip']})
        location = f"{get_location[0]['geometry']['location']['lat']},{get_location[0]['geometry']['location']['lng']}"
        return location

    def consolidate_response(self,locresponse):
        avail_list = []
        i = 0
        for place in locresponse['results']:
            if i < 3:
                avail_list.append({'name':place['name'], 'address':place['vicinity']})
            else:
                return avail_list
            i+=1
        return avail_list
    
    def create_query_string(self, age_req):
        qs = ''
        level = self.get_player_level(int(age_req))
        if level is None:
            qs = f'{PROJECT_SPORT} league'
        if level is GlobalLevels.T_BALL:
            qs = f'{level} league'
        else:
            qs = f'{level} league'
        return qs
