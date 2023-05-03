from django.urls import path
from . import views
urlpatterns = [
    path("glovesize/", views.GloveView.as_view()),
    path("batsize/", views.BatView.as_view()),
]