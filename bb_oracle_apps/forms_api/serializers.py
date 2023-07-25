from rest_framework import serializers
from .models import form

class FormSerializer(serializers.ModelSerializer):
    class Meta:
        model=form
        fields = ['form_type', 'submitter','submitter_email','submitter_phone','submitter_message']