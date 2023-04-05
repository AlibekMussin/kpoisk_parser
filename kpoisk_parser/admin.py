import csv
import datetime
import io
import openpyxl
from django.contrib import admin
from kpoisk_parser.models import Movie
from django.http import HttpResponse


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    search_fields = ['title_ru']
    list_filter = ['year']

    list_display = ('id',
                    'position_in_top',
                    'title_ru', 'title_en',
                    'year', 'length',
                    'created_at', 'updated_at')

    actions = ['download_movies_csv', 'download_movies_xlsx']

    def download_movies_csv(self, request, queryset):
        # Функция скачивания файла с ТОПом
        response = HttpResponse(content_type='text/csv')
        now = datetime.datetime.now().strftime("%d.%m.%Y")
        response['Content-Disposition'] = 'attachment; filename=kinopoisk_top_250{}.csv'.format(str(now))

        output = io.StringIO()
        writer = csv.writer(output, delimiter=',')
        writer.writerow(['Наименование на русском', 'Наименование на английском', 'Год выпуска', 'Продолжительность'])

        movies = Movie.objects.all().order_by('position_in_top')
        for movie in movies:
            writer.writerow([movie.title_ru, movie.title_en, movie.year, movie.length])
        response.write(output.getvalue().encode('cp1251'))
        return response

    download_movies_csv.short_description = 'Скачать фильмы в формате CSV'

    def download_movies_xlsx(self, request, queryset):
        # Функция скачивания файла с ТОПом
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = 'Movies'
        now = datetime.datetime.now().strftime("%d.%m.%Y")
        ws.append(['Наименование на русском', 'Наименование на английском', 'Год выпуска', 'Продолжительность'])

        movies = Movie.objects.all().order_by('position_in_top')
        for movie in movies:
            ws.append([movie.title_ru, movie.title_en, movie.year, movie.length])

        # Возвращение HttpResponse с файлом xlsx для скачивания
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=kinopoisk_top_250-{}.xlsx'.format(
            str(now)
        )
        wb.save(response)
        return response

    download_movies_xlsx.short_description = 'Скачать фильмы в формате xlsx'

