from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from .question_mixins import AIMessageMixIn
from .serializers import QuestionInfoSerializer
from base_ball_oracle.settings import OPEN_API_KEY, OPEN_AI_MODEL, PROJECT_SPORT
from base_ball_oracle.global_mixins import ValidateParamsMixIn
# Create your views here.

class Question(APIView,AIMessageMixIn,ValidateParamsMixIn):
    preq_val = f'Pretend you are a {PROJECT_SPORT} coach and explain the following in 8 sentences or less:'
    question_key = 'question'
    ai_key = OPEN_API_KEY
    ai_model = OPEN_AI_MODEL
    accepted_params = {'question':int.__name__}
    def get(self,request,*args,**kwargs):
        if self.validate_keys(request, 'all'):
            answer = self.ai_answer(request.query_params[self.get_question_key()])
            self.capture_question(answer,f'{self.preq_val} {request.query_params[self.get_question_key()]}')
            return Response(data={'answer':answer}, status=status.HTTP_200_OK)
        else:
            return Response(data={'error':'Invalid Params', 'available':self.get_accepted_params()}, status=status.HTTP_400_BAD_REQUEST)

    
    def capture_question(self,answer,request):
        serializer = QuestionInfoSerializer(data={'question_text':request, 'question_reply':answer})
        serializer.is_valid(raise_exception=True)
        serializer.save()
