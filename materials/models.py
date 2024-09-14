from django.db import models

import config.settings
import users.models

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name="Название курса",
        help_text="Введите название курса",
    )
    preview = models.ImageField(
        upload_to="materials/previews",
        verbose_name="Превью",
        **NULLABLE,
        help_text="Загрузите аватар"
    )
    description = models.TextField(
        verbose_name="Описание курса", **NULLABLE, help_text="Введите описание курса"
    )
    owner = models.ForeignKey(
        config.settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        **NULLABLE,
        verbose_name="Владелец",
        help_text="Укажите владельца"
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="lessons", verbose_name="Курс"
    )
    name = models.CharField(
        max_length=150,
        verbose_name="Название урока",
        help_text="Введите название урока",
    )
    description = models.TextField(
        verbose_name="Описание урока", **NULLABLE, help_text="Введите описание урока"
    )
    preview = models.ImageField(
        upload_to="materials/previews",
        verbose_name="Превью",
        **NULLABLE,
        help_text="Загрузите аватар"
    )
    video_url = models.URLField(
        verbose_name="Ссылка на видео", help_text="Введите ссылку на видео", **NULLABLE
    )
    owner = models.ForeignKey(
        config.settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        **NULLABLE,
        verbose_name="Владелец",
        help_text="Укажите владельца"
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.name
