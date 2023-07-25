from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import FormSerializer
from .models import form_type
# Create your views here.
class SubmitForm(CreateAPIView):
    serializer_class=FormSerializer

    def create(self,request,*args,**kwargs):
        request.data['form_type'] = self.get_form_type(request.data['form_type'])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def get_form_type(self,data):
        obj = form_type.objects.get(form_type=data)
        return obj.pk

