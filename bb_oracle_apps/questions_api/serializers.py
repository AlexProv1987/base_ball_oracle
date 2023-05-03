from rest_framework import serializers
from .models import questions
class QuestionInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model=questions
        fields = ['question_text', 'question_reply', 'request_date']