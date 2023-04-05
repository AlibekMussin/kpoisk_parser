from datetime import datetime
import requests
import csv
import  os
from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
from openpyxl import Workbook
from django.conf import settings
from kpoisk_parser.models import Movie


class Command(BaseCommand):
    help = "Parsing TOP 250"

    def add_arguments(self, parser):
        parser.add_argument('--file_format', nargs='+', type=str, help='final file format (takes arguments xlsx or csv)')

    def handle(self, *args, **kwargs):
        print("get TOP-250...")
        cookie = settings.COOKIE
        num = 0
        row_number = 1
        file_format = kwargs['file_format']
        # создаем новый экземпляр книги Excel
        workbook = Workbook()
        sheet = workbook.active
        # добавляем заголовки столбцов
        sheet["A1"] = "Название"
        sheet["B1"] = "Название на английском"
        sheet["C1"] = "Год выпуска"
        sheet["D1"] = "Продолжительность"

        if 'xlsx' in file_format:
            if os.path.exists("top250.xlsx"):
                os.remove("top250.xlsx")

        with open("top250.csv", "w", newline="") as csv_file:
            writer = csv.writer(csv_file, delimiter=",")

            writer.writerow(["Название", "Название на английском", "Год выпуска", "Продолжительность"])

            for page in range(1, 6):
                url = f"https://www.kinopoisk.ru/lists/movies/top250/?page={page}"
                response = requests.get(url, headers={"cookie": cookie, "content-type": "text/html; charset=utf-8"})
                soup = BeautifulSoup(response.text, "html.parser")
                span_elements = soup.find_all('div', class_=lambda x: x and x.startswith('styles_content__'))
                for movie in span_elements:

                    previous_div = movie.find_previous_sibling("div", class_=lambda x: x and x.startswith('styles_root__'))
                    previous_span = previous_div.find('span', class_=lambda x: x and x.startswith('styles_position__'))
                    position = int(previous_span.text)

                    # if num <= 16:
                    if num <= 260:
                        num += 1
                        row_number += 1
                        title = movie.find('span', class_=lambda x: x and x.startswith('styles_mainTitle'))
                        title_eng = movie.find('span', class_=lambda x: x and x.startswith('desktop-list-main-info_secondaryTitle__'))
                        year_length = movie.find('span', class_=lambda x: x and x.startswith('desktop-list-main-info_secondaryText_'))

                        year_length_text = str(year_length.text)
                        year_length_arr = year_length_text.split(', ')
                        year = ""
                        length = ""
                        # print(year_length_arr)
                        if len(year_length_arr) == 3:
                            year = year_length_arr[1]
                            length = year_length_arr[2]
                        elif len(year_length_arr) == 2:
                            year = year_length_arr[0]
                            length = year_length_arr[1]
                        title_eng_text = ""
                        if title_eng:
                            title_eng_text = title_eng.text
                        # print(f"{num}) {title.text} ({title_eng_text}), ({year}, {length})")
                        sheet[f"A{row_number}"] = title.text
                        sheet[f"B{row_number}"] = title_eng_text
                        sheet[f"C{row_number}"] = year
                        sheet[f"D{row_number}"] = length
                        # print(f"{num}, {title.text}")
                        title_eng_text_norm = title_eng_text.replace('é', 'e')
                        title_eng_text_norm = title_eng_text_norm.replace('è', 'e')
                        title_eng_text_norm = title_eng_text_norm.replace('û', 'u')
                        check_position = Movie.objects.filter(
                            position_in_top=position
                        ).last()
                        if check_position is None:
                            print("add new movie")
                            Movie.objects.create(
                                position_in_top=position,
                                title_ru=str(title.text),
                                title_en=title_eng_text_norm,
                                year=year,
                                length=length
                            )
                        else:
                            if check_position.title_ru != str(title.text):
                                print("update movie")
                                check_position.title_ru = str(title.text)
                                check_position.title_en = title_eng_text_norm
                                check_position.year = year
                                check_position.length = length
                                check_position.updated_at = datetime.now()
                                check_position.save()

                        # writer.writerow([str(title.text), title_eng_text_norm, year, length])

        if 'xlsx' in file_format:
            print("save to xlsx...")
            workbook.save(filename="top250.xlsx")

        if 'csv' in file_format:
            print("save to csv...")





