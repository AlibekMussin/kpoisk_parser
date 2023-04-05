from django.db import models


class Movie(models.Model):
    """ Организации """
    position_in_top = models.IntegerField(
        verbose_name="Место в ТОПе",
        null=True,
        blank=True
    )
    title_ru = models.CharField(
        max_length=1024,
        verbose_name="Наименование на русском",
        null=True,
        blank=True
    )
    title_en = models.CharField(
        max_length=1024,
        verbose_name="Наименование на английском",
        null=True,
        blank=True
    )
    year = models.IntegerField(
        verbose_name="Год выпуска",
        null=True,
        blank=True
    )
    length = models.CharField(
        max_length=250,
        verbose_name="Продолжительность",
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(
        verbose_name='Создано',
        auto_now_add=True,
        editable=False,
        null=True,
        blank=True
    )
    updated_at = models.DateTimeField(
        verbose_name='Обновлено',
        auto_now=True
    )

    def __str__(self):
        return str(self.title_ru)

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"