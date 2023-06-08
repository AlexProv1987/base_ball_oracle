from django.db import models

# Create your models here.
class searchedleagues(models.Model):
    total_found = models.IntegerField()
    zip_searched = models.IntegerField()
    sport_level = models.CharField(max_length=255, default='')
    age_searched = models.IntegerField(default = 0)
    search_date = models.DateField(auto_now=True)
    radius = models.IntegerField(default=25)
