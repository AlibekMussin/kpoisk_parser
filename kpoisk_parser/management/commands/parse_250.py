from datetime import datetime
import requests
import csv
import  os
from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
from openpyxl import Workbook

from kpoisk_parser.models import Movie


class Command(BaseCommand):
    help = "Parsing TOP 250"

    def add_arguments(self, parser):
        parser.add_argument('--file_format', nargs='+', type=str, help='final file format (takes arguments xlsx or csv)')

    def handle(self, *args, **kwargs):
        print("get TOP-250...")
        cookie = "_ym_uid=1672138804284025852; yandexuid=8701005031668666276; yuidss=8701005031668666276; yandex_login=; i=+KD8dX8Uuz3uKkdnpWuk32TyQdB1WOj1FQA9yXPAydvDz69yjGKJ7ogyw6ouqygtQfUmaL94hgjAqFMHqNc1oMpwFic=; desktop_session_key=419b1993e4055f6c14d4eb3bb102ec5cc642d09c2286fd9b6fb5ac84fadce755e5bb584d8fc941495e61c0cedae55c6394b943ecd3f28514460a65dc189702b136f7a6a8f8b406e5ea3d19ce9dbe02492b819a50a97958f22d2377cdd377c556; desktop_session_key.sig=D8zC8GXtnD5ZAY2-gtLUy9rWJmI; PHPSESSID=831e7ea04b123c367ffc3311a1f20ac0; yandex_gid=163; tc=5361; gdpr=0; _ym_isad=2; yp=1680672723.yu.8701005031668666276; ymex=1683178323.oyu.8701005031668666276; user-geo-region-id=163; user-geo-country-id=122; mda_exp_enabled=1; _csrf=fmNM4uT2iCIQ20FJy9tidUjc; disable_server_sso_redirect=1; ya_sess_id=noauth:1680594043; ys=c_chck.3762161043; mda2_beacon=1680594043657; sso_status=sso.passport.yandex.ru:synchronized; _yasc=yyZJv7gS/r8z/Wde/ejnDV40YOE3COy4XV3PGgZfIvzm9PRyyxe9YNhe0u3fww==; _ym_d=1680597282; cycada=ejaH7XKZGeSGHpf4PQ4FykY+VJwxpNicLZqNU2YECII="
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





