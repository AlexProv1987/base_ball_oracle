from django.contrib import admin

from bb_oracle_apps.league_finder.models import searchedleagues
from bb_oracle_apps.questions_api.models import questions
from bb_oracle_apps.web_scraper.models import product_type,scraped_product
# Register your models here.
class ScrapedProductAdmin(admin.ModelAdmin):
    list_display=['product_type_reltn', 'product_name','date_scraped','vendor']
class SearchedLeaguesAdmin(admin.ModelAdmin):
    list_display=['total_found','zip_searched','age_searched','sport_level', 'search_date', 'radius']
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['request_date', 'question_text',]
admin.site.register(product_type)
admin.site.register(scraped_product, ScrapedProductAdmin)
admin.site.register(searchedleagues,SearchedLeaguesAdmin)
admin.site.register(questions,QuestionAdmin)