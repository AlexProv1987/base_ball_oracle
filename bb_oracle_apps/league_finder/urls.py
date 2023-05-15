from django.urls import path
from . import views
urlpatterns = [
    path("findleague/", views.LeagueFinder.as_view()),
]