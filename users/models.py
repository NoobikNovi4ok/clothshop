import uuid
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        if email is None:
            short_id = str(uuid.uuid4().hex[:6])  # Берем первые 6 символов UUID
            email = f"superuser_{short_id}@example.com"  # Генерация компактного email
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)

    def get_by_natural_key(self, login):
        return self.get(login=login)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(
        max_length=50,
        validators=[
            RegexValidator(
                regex=r"^[А-Яа-яЁё\s-]+$",
                message="Имя может содержать только кириллицу, пробелы и тире.",
            )
        ],
        verbose_name="Имя",
    )
    surname = models.CharField(
        max_length=50,
        validators=[
            RegexValidator(
                regex=r"^[А-Яа-яЁё\s-]+$",
                message="Фамилия может содержать только кириллицу, пробелы и тире.",
            )
        ],
        verbose_name="Фамилия",
    )
    patronymic = models.CharField(
        max_length=50,
        blank=True,
        validators=[
            RegexValidator(
                regex=r"^[А-Яа-яЁё\s-]*$",
                message="Отчество может содержать только кириллицу, пробелы и тире.",
            )
        ],
        verbose_name="Отчество",
    )
    login = models.CharField(
        max_length=40,
        unique=True,
        validators=[
            RegexValidator(
                regex=r"^[a-zA-Z0-9-]+$",
                message="Логин может содержать только латиницу, цифры и тире.",
            )
        ],
        verbose_name="Логин",
    )
    email = models.EmailField(unique=True, max_length=60, verbose_name="Почта")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "login"
    REQUIRED_FIELDS = ["name", "surname"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.name} {self.surname} {self.patronymic}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
