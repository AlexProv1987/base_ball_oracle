from rest_framework import serializers
from .models import product_type,scraped_product

class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = product_type
        fields = ['product_type']
        
class ScrapedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=scraped_product
        fields = ['product_type_reltn', 'product_name', 'vendor', 'date_scraped']

#this is somewhat embarassingly lazy, but I need to dig into how to have this serializer interact properly
#between saving and displaying data
class ScrapedProductViewSerializer(serializers.ModelSerializer):
    product_type_reltn = ProductTypeSerializer()
    class Meta:
        model = scraped_product
        fields = ['product_type_reltn', 'product_name', 'vendor', 'date_scraped']