from django.db import models
# Create your models here.
class product_type(models.Model):
    product_type = models.CharField(max_length=50)
    
class scraped_product(models.Model):
    product_name = models.CharField(max_length=175)
    date_scraped = models.DateField(auto_now=True)
    product_type = models.ForeignKey(product_type, on_delete=models.PROTECT)
    vendor = models.CharField(max_length=75)