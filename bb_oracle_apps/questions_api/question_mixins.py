import openai
from rest_framework.response import Response
from rest_framework import status
import time
class AIMessageMixIn():
    preq_val = ''
    ai_key = None
    ai_model = None
    tokens = 1024
    sleep_internal = 200
    temp = 0
    question_key = None
    role = 'user'

    def get(self,request,*args,**kwargs):
        return Response(data=self.ai_answer(request.data[self.get_question_key()]), status=status.HTTP_200_OK)
    
    def ai_answer(self, question):
        #sleep is built in to avoid exceeding the normal 60rpm
        time.sleep(self.sleep_internal/1000)
        openai.api_key = self.get_ai_key()
        response_msg = openai.ChatCompletion.create(
        #different models have different capabilities
        model = self.get_ai_model(),
        #length of response
        max_tokens=self.tokens,
        #determinism level lower is more
        temperature = self.temp,
        messages = [{
            'role':self.role,
            'content': f'{self.preq_val} {question}?',
        }],
        )
        return response_msg['choices'][0]['message']['content']
    
    def get_question_key(self):
        question_key = self.question_key
        assert self.question_key is not None,(
            "'%s'Should include question_key or override 'get_question_key()' method."
            % self.__class__.__name__
        )
        return question_key
    
    def get_ai_model(self):
        ai_model = self.ai_model
        assert self.question_key is not None,(
            "'%s'Should include ai_model or override 'get_ai_model()' method."
            % self.__class__.__name__
        )
        return ai_model
    
    def get_ai_key(self):
        ai_key = self.ai_key
        assert self.ai_key is not None,(
            "'%s'Should include ai_key or override 'get_ai_key()' method."
            % self.__class__.__name__
        )
        return ai_key