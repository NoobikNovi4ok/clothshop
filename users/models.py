from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(
        max_length=30,
        validators=[
            RegexValidator(
                regex=r"^[А-Яа-яЁё\s-]+$",
                message="Имя может содержать только кириллицу, пробелы и тире.",
            )
        ],
    )
    surname = models.CharField(
        max_length=30,
        validators=[
            RegexValidator(
                regex=r"^[А-Яа-яЁё\s-]+$",
                message="Фамилия может содержать только кириллицу, пробелы и тире.",
            )
        ],
    )
    patronymic = models.CharField(
        max_length=30,
        blank=True,
        validators=[
            RegexValidator(
                regex=r"^[А-Яа-яЁё\s-]*$",
                message="Отчество может содержать только кириллицу, пробелы и тире.",
            )
        ],
    )
    login = models.CharField(
        max_length=30,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z0-9-]+$",
                message="Логин может содержать только латиницу, цифры и тире.",
            )
        ],
    )
    email = models.EmailField(unique=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.name}"
