from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from .question_mixins import AIMessageMixIn
from .serializers import QuestionInfoSerializer
from .models import questions
from base_ball_oracle.settings import OPEN_API_KEY, OPEN_AI_MODEL, PROJECT_SPORT
# Create your views here.

class Question(APIView,AIMessageMixIn):
    preq_val = f'Pretend you are a {PROJECT_SPORT} coach and explain the following in three sentences:'
    question_key = 'question'
    ai_key = OPEN_API_KEY
    ai_model = OPEN_AI_MODEL

    def get(self,request,*args,**kwargs):
        answer = self.ai_answer(request.data[self.get_question_key()])
        self.capture_question(answer,f'{self.preq_val} {request.data[self.get_question_key()]}')
        return Response(data=self.ai_answer(request.data[self.get_question_key()]), status=status.HTTP_200_OK)
    
    def capture_question(self,answer,request):
        serializer = QuestionInfoSerializer(data={'question_text':request, 'question_reply':answer})
        serializer.is_valid(raise_exception=True)
        serializer.save()

class QuestionData(ListAPIView):
    queryset=questions.objects.all()
    serializer_class=QuestionInfoSerializer