from django.contrib import admin
from kpoisk_parser.models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    search_fields = ['title_ru']
    list_filter = ['year']

    list_display = ('id',
                    'position_in_top',
                    'title_ru', 'title_en',
                    'year', 'length','created_at','updated_at')
