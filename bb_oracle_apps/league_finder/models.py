from django.db import models

# Create your models here.
class searchedleagues(models.Model):
    total_found = models.IntegerField()
    zip_searched = models.IntegerField()
    search_date = models.DateField(auto_now=True)
    radius = models.IntegerField(default=25)