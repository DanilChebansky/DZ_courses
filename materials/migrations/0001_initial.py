# Generated by Django 4.2.2 on 2024-09-03 19:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Введите название курса",
                        max_length=150,
                        verbose_name="Название курса",
                    ),
                ),
                (
                    "preview",
                    models.ImageField(
                        blank=True,
                        help_text="Загрузите аватар",
                        null=True,
                        upload_to="materials/previews",
                        verbose_name="Превью",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="Введите описание курса",
                        null=True,
                        verbose_name="Описание курса",
                    ),
                ),
            ],
            options={
                "verbose_name": "Курс",
                "verbose_name_plural": "Курсы",
            },
        ),
        migrations.CreateModel(
            name="Lesson",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Введите название урока",
                        max_length=150,
                        verbose_name="Название урока",
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="Введите описание урока",
                        null=True,
                        verbose_name="Описание урока",
                    ),
                ),
                (
                    "preview",
                    models.ImageField(
                        blank=True,
                        help_text="Загрузите аватар",
                        null=True,
                        upload_to="materials/previews",
                        verbose_name="Превью",
                    ),
                ),
                (
                    "video_url",
                    models.URLField(
                        blank=True,
                        help_text="Введите ссылку на видео",
                        null=True,
                        verbose_name="Ссылка на видео",
                    ),
                ),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="lessons",
                        to="materials.course",
                        verbose_name="Курс",
                    ),
                ),
            ],
            options={
                "verbose_name": "Урок",
                "verbose_name_plural": "Уроки",
            },
        ),
    ]
