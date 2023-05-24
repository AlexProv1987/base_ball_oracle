from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .equip_sizes import GloveSize, BatSize
from base_ball_oracle.global_mixins import ValidateParamsMixIn
# Create your views here.

class GloveView(APIView,GloveSize, ValidateParamsMixIn):
    accepted_params = {'age':int.__name__, 'position':str.__name__}
    def get(self,request,*args,**kwargs):
        if self.validate_keys(request, 'all'):
            self.set_player_level(int(request.query_params['age']))
            return Response(data={
                'level': self.player_level, 
                'size':self.get_glove_size(request.query_params['position'])}, 
                status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class BatView(APIView, BatSize,ValidateParamsMixIn):
    accepted_params = {'height':str.__name__, 'weight':int.__name__}
    def get(self,request,*args,**kwargs):
        if self.validate_keys(request, 'all'):
            bat = self.get_bat_size(int(request.query_params['height']),int(request.query_params['weight']))
            if bat is None:
                return Response(data ={'bat_size':'None Found'}
                            ,status=status.HTTP_200_OK)
            return Response(data ={'bat_size':bat}
                        ,status=status.HTTP_200_OK)
        else:
            return Response(data={'error':'Invalid Params', 'available':self.get_accepted_params()}, status=status.HTTP_400_BAD_REQUEST)