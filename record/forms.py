from django import forms
from django.contrib.auth import get_user_model

from .models import Category, Record, Status, Tag


class RecordForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.filter(
            author=self.request.user
        )
        self.fields["status"].queryset = Status.objects.filter(author=self.request.user)
        self.fields["tags"].queryset = Tag.objects.filter(author=self.request.user)

    class Meta:
        model = Record
        fields = ["title", "body", "category", "status", "tags"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "body": forms.Textarea(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "tags": forms.SelectMultiple(attrs={"class": "form-select"}),
        }
        labels = {
            "title": "Заголовок",
            "body": "Описание",
            "category": "Категория",
            "status": "Статус",
            "tags": "Тэги",
        }


class NameForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
        }
        labels = {
            "name": "Название категории",
        }
        error_messages = {
            "name": {
                "unique": "Категория с таким названием уже существует!",
            }
        }
