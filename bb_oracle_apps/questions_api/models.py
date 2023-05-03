from django.db import models
# Create your models here.
class questions(models.Model):
    question_text = models.TextField(max_length=1024)
    request_date = models.DateField(auto_now=True)
    question_reply = models.TextField(max_length=1024)