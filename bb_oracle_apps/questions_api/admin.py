from django.contrib import admin
from bb_oracle_apps.league_finder.models import searchedleagues
from bb_oracle_apps.questions_api.models import questions
# Register your models here.
admin.site.register(searchedleagues)
admin.site.register(questions)