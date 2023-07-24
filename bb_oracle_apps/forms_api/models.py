from django.db import models
# Create your models here.
class form_type(models.Model):
    form_type = models.CharField(max_length=20)

    def __str__(self):
        return self.form_type

class form(models.Model):
    form_type = models.ForeignKey(form_type, on_delete=models.PROTECT)
    submitter = models.CharField(max_length=100)
    submitter_email = models.EmailField()
    #from django.core.validators import RegexValidator r'^\+?1?\d{9,15}$' well add a reg ex validator since there isnt a default one for django
    submitter_phone = models.CharField(max_length=17, null=True, blank=True)
    submitter_message = models.TextField(max_length=500, null=True, blank=True)
    followed_up = models.BooleanField(default=False)
    submit_date_tm = models.DateField(auto_now_add=True)