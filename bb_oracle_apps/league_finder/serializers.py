from rest_framework import serializers
from .models import searchedleagues
class SearchedLeaugesSerializer(serializers.ModelSerializer):
    class Meta:
        model=searchedleagues
        fields = ['total_found', 'zip_searched', 'search_date']