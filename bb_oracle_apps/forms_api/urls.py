from django.urls import path
from . import views
urlpatterns = [
    path("submit/", views.SubmitForm.as_view()),
]