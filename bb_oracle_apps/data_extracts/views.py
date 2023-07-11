from rest_framework import generics
from bb_oracle_apps.league_finder.models import searchedleagues
from bb_oracle_apps.league_finder.serializers import SearchedLeaugesSerializer
from bb_oracle_apps.questions_api.models import questions
from bb_oracle_apps.questions_api.serializers import QuestionInfoSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .filters import QuestionFilter, LeagueFilter, ProductFilter
from bb_oracle_apps.web_scraper.models import scraped_product
from bb_oracle_apps.web_scraper.serializers import ScrapedProductViewSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class QuestionHist(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset=questions.objects.all()
    serializer_class=QuestionInfoSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_class = QuestionFilter
    search_fields = ['question_text',]

class LeagueHist(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = searchedleagues.objects.all()
    serializer_class = SearchedLeaugesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = LeagueFilter

class ProductHist(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = scraped_product.objects.all()
    serializer_class = ScrapedProductViewSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['vendor',]
