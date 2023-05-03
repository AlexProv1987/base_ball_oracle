from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .equip_sizes import GloveSize, BatSize
# Create your views here.

class GloveView(APIView,GloveSize):
    def get(self,request,*args,**kwargs):
        self.set_player_level(int(request.data['age']))
        return Response(data={
            'level': self.player_level, 
            'size':self.get_glove_size(request.data['position'])}, 
            status=status.HTTP_200_OK)

class BatView(APIView, BatSize):
    def get(self,request,*args,**kwargs):
        bat = self.get_bat_size(int(request.data['height']),int(request.data['weight']))
        if bat is None:
            return Response(data ={'bat_size':'None Found'}
                            ,status=status.HTTP_200_OK)
        return Response(data ={'bat_size':bat}
                        ,status=status.HTTP_200_OK)