from typing import Type
from django import forms
from django.contrib import messages
from django.db import IntegrityError, models
from django.http import HttpRequest
from django.template.defaultfilters import slugify
from unidecode import unidecode


def get_name_form_or_get_form_and_add_row_into_db(
    request: HttpRequest,
    model: type[models.Model],
    item_name_label: str,
    item_name_error: str,
):
    if request.method == "POST":
        name_form = get_modelfrom_from_factory(model, item_name_label, item_name_error)
        name_form_instance = name_form(data=request.POST)

        if name_form_instance.is_valid():
            row = name_form_instance.save(commit=False)
            row.author = request.user
            row.slug = slugify(unidecode(row.name) + "_" + row.author.username)
            print(f"{slugify(unidecode(row.name) + '_' + row.author.username)=}")
            try:
                row.save()
            except IntegrityError:
                messages.add_message(
                    request, messages.INFO, "Не удалось сохранить данную категорию"
                )

            return None, True
    else:
        form = get_modelfrom_from_factory(model, item_name_label, item_name_error)
        name_form_instance = form()

    return name_form_instance, False


def get_modelfrom_from_factory(
    model, item_name_label: str | None = None, item_name_error: str | None = None
):
    return forms.modelform_factory(
        model=model,
        fields=["name"],
        widgets={
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
        },
        labels={
            "name": f"Название {item_name_label}",
        },
        error_messages={
            "name": {
                "unique": f"{item_name_error.capitalize()} с таким названием уже существует!",
            }
        },
    )
