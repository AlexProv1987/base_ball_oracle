from django.urls import path
from . import views
urlpatterns = [
    path("ask/", views.Question.as_view()),
]