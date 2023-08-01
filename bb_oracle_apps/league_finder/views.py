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
#this all looks kind of messy as it stands now and not super readable
class LeagueFinder(APIView,GlobalLevels,ValidateParamsMixIn):
    google_maps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
    accepted_params = {'age':int.__name__, 'zip':int.__name__}
    level_chart = {
        GlobalLevels.T_BALL:range(0,7),
        'all': range(7,100)
    }

    def get(self,request,*args,**kwargs):
        #validate we have all required params in the request
        if self.validate_keys(request, 'all'):
            #call main class method to return available locations
            avail_places = self._get_avail_options(request)
            if avail_places is None:
                return Response(data={'error':'Invalid Zip Code'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data={'totalplaces':len(avail_places), 'places':avail_places}, status=status.HTTP_200_OK)
        else:
            return Response(data={'error':'Invalid Params', 'available':self.get_accepted_params()}, status=status.HTTP_400_BAD_REQUEST)
    
    #main class method to return a list of dicts with available places and their details
    def _get_avail_options(self,request):
        #list for place_id's
        avail_list = []
        #start as none for our detailed_place return var until we append dicts in _return_place_details()
        detailed_places = None
        #attempt to get cordinates of the zip code provided
        geolocation = self._get_person_location(request.query_params['zip'])
        
        #if we failed to get cordinates return
        if geolocation is None:
            return detailed_places

        level = self.get_player_level(int(request.query_params['age']))
        qs = self._create_query_string(level)

        #declare end_radius to store how far out we had to go to find 3 valid locations
        end_radius = None

        #start idx is 5, incrimenting by 5, until less than 26(25)
        #this allows us to start at 5miles from the location and expand outward as needed to 25
        for i in range(5,26,5):
            #if we have found 3 good results already, we can break out of our loop
            if len(avail_list) >= 3:
                break
            #send request to googlemaps api
            places = self.google_maps.places_nearby(
            keyword=qs, 
            location=geolocation,
            radius=ConvertValue.convert(i,1609),
            language='en-US',
            )
            #filter the response and reset avail_list
            avail_list = self._filter_response(places, avail_list)
            #set the end radius to the value of the current index
            end_radius = i
        #once we have found 3 suitable results and appended their ID's to the avail_list variable, get the business details.
        detailed_places = self._return_place_details(avail_list)
        #capture the request
        self.capture_request(radius=end_radius,
                            total_found=len(avail_list),
                            zip_searched=request.query_params['zip'],
                            sport_level=level,
                            age_searched=request.query_params['age'])
        #return list of dicts
        return detailed_places
    
    #geolocate and return cordinates, if none zip code wasnt a valid zip -> front end should implement a lib to validate there as well
    def _get_person_location(self,zip):
        try:
            get_location = self.google_maps.geocode(zip)
            location = f"{get_location[0]['geometry']['location']['lat']},{get_location[0]['geometry']['location']['lng']}"
            return location
        except:
            return None
        
   #filter results to only select ones with baseball in title, append and return avail_list passed in
    def _filter_response(self,locresponse, avail_list):
        for place in locresponse['results']:
                if len(avail_list) < 3:
                    #if it contains baseball and the place_id doesnt currently exist in our avail_list append
                    if 'baseball' in place['name'].lower() and place['place_id'] not in avail_list:
                        avail_list.append(place['place_id'])
        return avail_list
    
    #for each place id passed in, return place details
    def _return_place_details(self, places):
        place_details = []
        #for each place(id) we must make a request to get its details
        for place in places:
            #phone and web are not guarnteed so we must check to avoid key errors
            phone_num = 'Not Available'
            web_site = 'Not Available'
            #make API call
            p_detail = self.google_maps.place(place_id=place)
            if 'formatted_phone_number' in p_detail['result']:
                phone_num = p_detail['result']['formatted_phone_number']
            if 'website' in p_detail['result']:
                web_site = p_detail['result']['website']
            #append a new dict to the list
            place_details.append({'name':p_detail['result']['name'],'address':p_detail['result']['formatted_address'],'phone': phone_num,'website':web_site})
        #return the list of dicts
        return place_details

    #create our search string based on level and return
    def _create_query_string(self, level):
        qs = ''
        if level is GlobalLevels.T_BALL:
            qs = f'{level} league'
        else:
            qs = f'{PROJECT_SPORT} league'
        return qs
    
    #capture the request to DB (can probably just implement CreateView generic instead)
    def capture_request(self,**kwargs):
        serializer = SearchedLeaugesSerializer(data=kwargs)
        serializer.is_valid(raise_exception=True)
        serializer.save()
