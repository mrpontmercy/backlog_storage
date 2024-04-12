from django import forms
from django.contrib.auth import get_user_model


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(label="Логин")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput())
    password2 = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password",
            "password2",
        ]
        labels = {
            "email": "E-mail:",
            "first_name": "Имя:",
            "last_name": "Фамилия",
        }

    # https://docs.djangoproject.com/en/5.0/topics/forms/modelforms/
    def clean_password2(
        self,
    ):  # clean_field позволяет сделать дополнительную валидацию указанного поля
        data = self.cleaned_data
        if data["password"] != data["password2"]:
            raise forms.ValidationError("Пароли не совпадают")
        return data["password"]

    # def clean_email(self):
    #     email = self.cleaned_data["email"]
    #     if get_user_model().objects.filter(email=email).exists():
    #         raise forms.ValidationError("Пользователь с таким Email уже существует!")
    #     return email
