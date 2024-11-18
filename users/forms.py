import re
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from users.models import User


class UserRegistrationForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-2",
                "id": "name",
                "name": "name",
                "placeholder": "Name",
                "autocomplete": "Name",
            }
        ),
        max_length=50,
        required=True,
        error_messages={"required": "Это поле обязательно."},
        label="Имя",
    )

    surname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-2",
                "id": "surname",
                "name": "surname",
                "placeholder": "Surname",
                "autocomplete": "Surname",
            }
        ),
        max_length=50,
        required=True,
        error_messages={"required": "Это поле обязательно."},
        label="Фамилия",
    )

    patronymic = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-2",
                "id": "patronymic",
                "name": "patronymic",
                "placeholder": "Patronymic",
                "autocomplete": "Patronymic",
            }
        ),
        max_length=50,
        required=False,
        label="Отчество",
    )

    login = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-2",
                "id": "login",
                "name": "login",
                "placeholder": "Login",
                "autocomplete": "Login",
            }
        ),
        max_length=40,
        required=True,
        error_messages={"required": "Это поле обязательно."},
        label="Логин",
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control mb-2",
                "id": "email",
                "name": "email",
                "placeholder": "name@example.com",
                "autocomplete": "example@gmail.com",
            }
        ),
        required=True,
        error_messages={
            "required": "Это поле обязательно.",
            "invalid": "Введите корректный email.",
        },
        label="Почта",
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control mb-2",
                "id": "password",
                "name": "Password",
                "placeholder": "Password",
                "autocomplete": "Password",
            }
        ),
        min_length=6,
        required=True,
        error_messages={"required": "Это поле обязательно."},
        label="Пароль",
    )

    password_repeat = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control mb-2",
                "id": "password_repeat",
                "name": "password_repeat",
                "placeholder": "Password_repeat",
                "autocomplete": "Password_repeat",
            }
        ),
        required=True,
        error_messages={"required": "Это поле обязательно."},
        label="Подтверждение пароля",
    )

    rules = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input mb-2", "id": "rules"}
        ),
        required=True,
        error_messages={"required": "Вы должны согласиться с правилами регистрации."},
        label="Согласие с правилами регистрации",
    )

    class Meta:
        model = User
        fields = [
            "name",
            "surname",
            "patronymic",
            "login",
            "email",
            "password",
            "password_repeat",
            "rules",
        ]

    def clean_name(self):
        name = self.cleaned_data["name"]
        if not re.match(r"^[а-яА-ЯёЁ\s-]+$", name):
            raise ValidationError(
                _("Имя может содержать только кириллицу, пробелы и тире.")
            )
        return name

    def clean_surname(self):
        surname = self.cleaned_data["surname"]
        if not re.match(r"^[а-яА-ЯёЁ\s-]+$", surname):
            raise ValidationError(
                _("Фамилия может содержать только кириллицу, пробелы и тире.")
            )
        return surname

    def clean_login(self):
        login = self.cleaned_data["login"]
        if User.objects.filter(login=login).exists():
            raise forms.ValidationError(
                "Этот логин уже занят. Пожалуйста, введите другой."
            )
        if not re.match(r"^[a-zA-Z0-9-]+$", login):
            raise ValidationError(
                _("Логин может содержать только латиницу, пробелы и тире.")
            )
        return login

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Эта почта уже занята. Пожалуйста, введите другую."
            )
        return email

    def clean_password_repeat(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_repeat = cleaned_data.get("password_repeat")

        if password and password_repeat and password != password_repeat:
            raise ValidationError(_("Пароли не совпадают."))

        return password_repeat

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(
            self.cleaned_data["password"]
        )  # Устанавливаем зашифрованный пароль
        if commit:
            user.save()
        return user


User = get_user_model()


class UserLoginForm(AuthenticationForm):
    login = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control mb-2",
                "id": "login",
                "name": "login",
                "placeholder": "Login",
                "autocomplete": "Login",
            }
        ),
        max_length=40,
        required=True,
        error_messages={"required": "Это поле обязательно."},
        label="Логин",
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control mb-2",
                "id": "password",
                "name": "Password",
                "placeholder": "Password",
                "autocomplete": "Password",
            }
        ),
        required=True,
        error_messages={"required": "Это поле обязательно."},
        label="Пароль",
    )

    error_messages = {
        "invalid_login": "Неверный логин или пароль. Пожалуйста, попробуйте снова."
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"] = self.fields.pop("login")

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            self.user_cache = self.authenticate(username=username, password=password)
            if self.user_cache is None:
                raise ValidationError(
                    self.error_messages["invalid_login"],
                    code="invalid_login",
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(login=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
