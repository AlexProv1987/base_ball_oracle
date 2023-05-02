from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import openai
from base_ball_oracle.settings import OPEN_API_KEY, OPEN_AI_MODEL
# Create your views here.

class Question(APIView):

    def get(self,request,*args,**kwargs):
        age = request.data['age']
        question = request.data['question']
        openai.api_key = OPEN_API_KEY
        response_msg = openai.ChatCompletion.create(
        #different models have different capabilities
        model = OPEN_AI_MODEL,
        #length of response
        max_tokens=1024,
        #determinism level lower is more
        temperature = 0,
        messages = [{
            'role':'user',
            'content': f'For a {age} year old, {question}?',
        }],
        )
        return Response(data=response_msg.choices[0].message.content, status=status.HTTP_200_OK)