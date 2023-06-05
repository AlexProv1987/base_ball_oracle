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
class LeagueFinder(APIView,GlobalLevels,ValidateParamsMixIn):

    google_maps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
    accepted_params = {'age':int.__name__, 'zip':int.__name__}
    level_chart = {
        't-ball':range(0,7)
    }
    def get(self,request,*args,**kwargs):
        if self.validate_keys(request, 'all'):
            avail_places = self.get_avail_options(request)
            if avail_places is None:
                return Response(data={'error':'Invalid Zip Code'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data={'totalplaces':len(avail_places), 'places':avail_places}, status=status.HTTP_200_OK)
        else:
            return Response(data={'error':'Invalid Params', 'available':self.get_accepted_params()}, status=status.HTTP_400_BAD_REQUEST)
    
    def get_avail_options(self,request):
        detailed_places = None
        geolocation = self.get_person_location(request.query_params['zip'])
        
        if geolocation is None:
            return detailed_places
        else:
            level = self.get_player_level(int(request.query_params['age']))
            places = self.google_maps.places_nearby(
                    keyword=self.create_query_string(level), 
                    location=self.get_person_location(request.query_params['zip']),
                    radius=ConvertValue.convert(25,1609),
                    language='en-US',
                    )

            self.capture_request(kwargs={'age_searched':request.query_params['zip'],
                                    'total_found':len(places['results']),
                                    'zip_searched':request.query_params['zip'],
                                    'sport_level':level,
                                    'age_searched':request.query_params['age']})
        
            place_ids = self.consolidate_response(places)
            detailed_places = self.return_place_details(place_ids)
        return detailed_places
    
    def get_person_location(self,zip):
        try:
            get_location = self.google_maps.geocode(zip)
            location = f"{get_location[0]['geometry']['location']['lat']},{get_location[0]['geometry']['location']['lng']}"
            return location
        except:
            return None
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
            web_site = 'Not Available'
            p_detail = self.google_maps.place(place_id=place)
            if 'formatted_phone_number' in p_detail['result']:
                phone_num = p_detail['result']['formatted_phone_number']
            if 'website' in p_detail['result']:
                web_site = p_detail['result']['website']
            place_details.append({'name':p_detail['result']['name'],'address':p_detail['result']['formatted_address'],'phone': phone_num,'website':web_site})
        return place_details

    def create_query_string(self, level):
        qs = ''
        if level is GlobalLevels.T_BALL:
            qs = f'{level} league'
        else:
            qs = f'{PROJECT_SPORT} league'
        return qs
    

    def capture_request(self,**kwargs):
        serializer = SearchedLeaugesSerializer(data=kwargs['kwargs'])
        serializer.is_valid(raise_exception=True)
        serializer.save()
