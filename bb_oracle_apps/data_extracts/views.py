from rest_framework import generics
from bb_oracle_apps.league_finder.models import searchedleagues
from bb_oracle_apps.league_finder.serializers import SearchedLeaugesSerializer
from bb_oracle_apps.questions_api.models import questions
from bb_oracle_apps.questions_api.serializers import QuestionInfoSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .filters import QuestionFilter, LeagueFilter
from base_ball_oracle.global_mixins import ValidateParamsMixIn
class QuestionHist(generics.ListAPIView):
    queryset=questions.objects.all()
    serializer_class=QuestionInfoSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_class = QuestionFilter
    search_fields = ['question_text',]

class LeagueHist(generics.ListAPIView):
    queryset = searchedleagues.objects.all()
    serializer_class = SearchedLeaugesSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = LeagueFilter