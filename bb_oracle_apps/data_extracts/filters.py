import django_filters
from bb_oracle_apps.questions_api.models import questions
from bb_oracle_apps.league_finder.models import searchedleagues
from bb_oracle_apps.web_scraper.models import scraped_product
class QuestionFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='request_date', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='request_date', lookup_expr='lte')

    class Meta:
        model = questions
        fields = ['start_date', 'end_date']

class LeagueFilter(django_filters.FilterSet):
    zip_start = django_filters.NumberFilter(field_name='zip_searched', lookup_expr='gte')
    zip_end = django_filters.NumberFilter(field_name='zip_searched', lookup_expr='lte')
    sport_level = django_filters.CharFilter(field_name='sport_level', lookup_expr='exact')
    radius = django_filters.NumberFilter(field_name='radius', lookup_expr='gte')
    search_date_start = django_filters.DateFilter(field_name='search_date', lookup_expr='gte')
    search_date_end = django_filters.DateFilter(field_name='search_date', lookup_expr='lte')
    age_range_start = django_filters.NumberFilter(field_name='age_searched', lookup_expr='gte')
    age_range_end = django_filters.NumberFilter(field_name='age_searched', lookup_expr='lte')
    leagues_found = django_filters.NumberFilter(field_name='total_found', lookup_expr='lte')
    class Meta:
        model = searchedleagues
        fields = ['zip_start','zip_end', 'sport_level','radius','search_date_start','search_date_end','age_range_start','age_range_end', 'leagues_found',]

class ProductFilter(django_filters.FilterSet):
    search_date_start = django_filters.DateFilter(field_name='date_scraped', lookup_expr='gte')
    search_date_end = django_filters.DateFilter(field_name='date_scraped', lookup_expr='lte')
    product_type = django_filters.CharFilter(field_name='product_type_reln.product_type', lookup_expr='icontains')
    class Meta:
        model = scraped_product
        fields = ['search_date_start', 'search_date_end', 'product_type']