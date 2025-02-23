from django import forms


class CreateOrderForm(forms.Form):
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
    login = forms.CharField(
        widget=forms.HiddenInput(
            attrs={
                "class": "d-none",
                "id": "login",
                "name": "login",
                "placeholder": "login",
                "autocomplete": "login",
            }
        ),
        required=True,
        label="Пользователь",
    )
