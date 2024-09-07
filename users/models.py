from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email")

    avatar = models.ImageField(
        upload_to="users/avatars",
        verbose_name="Аватар",
        **NULLABLE,
        help_text="Загрузите аватар"
    )
    phone = models.CharField(
        max_length=35,
        verbose_name="Телефон",
        **NULLABLE,
        help_text="Введите номер телефона"
    )
    city = models.CharField(
        max_length=100, verbose_name="Город", **NULLABLE, help_text="Введите город"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    WAYS = [(1, "Наличные"), (2, "Перевод")]
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="Пользователь",
    )
    pay_date = models.DateField(verbose_name="Дата оплаты", auto_now_add=True)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="Оплаченный курс",
        **NULLABLE
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="Оплаченный урок",
        **NULLABLE
    )
    payment_sum = models.IntegerField(verbose_name="Сумма оплаты")
    payment_way = models.IntegerField(
        choices=WAYS, default=1, verbose_name="Способ оплаты"
    )
