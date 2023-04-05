from django.contrib import admin
from kpoisk_parser.models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    search_fields = ['title_ru']
    list_display = ('id',
                    'title_ru', 'title_en',
                    'year', 'length')
