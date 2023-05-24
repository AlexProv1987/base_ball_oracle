from django.shortcuts import render
from rest_framework import generics
from bb_oracle_apps.league_finder.models import searchedleagues
from bb_oracle_apps.league_finder.serializers import SearchedLeaugesSerializer
from bb_oracle_apps.questions_api.models import questions
from bb_oracle_apps.questions_api.serializers import QuestionInfoSerializer

class QuestionHist(generics.ListAPIView):
    queryset=questions.objects.all()
    serializer_class=QuestionInfoSerializer

class LeagueHist(generics.ListAPIView):
    queryset = searchedleagues.objects.all()
    serializer_class = SearchedLeaugesSerializer