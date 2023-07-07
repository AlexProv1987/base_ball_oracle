from django.urls import path
from . import views
urlpatterns = [
    path("league_hist/", views.LeagueHist.as_view()),
    path("question_hist/", views.QuestionHist.as_view()),
    path("product_hist/", views.ProductHist.as_view()),
]