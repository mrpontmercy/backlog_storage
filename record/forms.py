from django import forms

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
        fields = ["title", "body", "link_to_resource", "category", "status", "tags"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control m-2"}),
            "body": forms.Textarea(attrs={"class": "form-control m-2"}),
            "link_to_resource": forms.TextInput(attrs={"class": "form-control m-2"}),
            "category": forms.Select(attrs={"class": "form-select m-2"}),
            "status": forms.Select(attrs={"class": "form-select m-2"}),
            "tags": forms.SelectMultiple(attrs={"class": "form-select m-2"}),
        }
        labels = {
            "title": "Заголовок",
            "body": "Описание",
            "link_to_resource": "URL ресурса",
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
