from typing import Type
from django import forms
from django.contrib import messages
from django.db import IntegrityError, models
from django.http import HttpRequest
from django.template.defaultfilters import slugify
from unidecode import unidecode

from record.forms import NameForm


def add_row_with_slug_to_db(request: HttpRequest, model_instance: models.Model):
    if request.method == "POST":
        form = get_form(NameForm, model_instance, request.POST)

        if form.is_valid():
            row = form.save(commit=False)
            row.author = request.user
            row.slug = slugify(unidecode(row.name) + "_" + row.author.username)
            try:
                row.save()
            except IntegrityError:
                messages.add_message(
                    request, messages.INFO, "Не удалось сохранить данную категорию"
                )

            return None, True
    else:
        form = get_form(NameForm, instance=model_instance)

    return form, False


def get_form(obj: Type[forms.ModelForm], instance, data=None):
    return obj(data=data, instance=instance)


def delete_obj_with_sluh(obj_string): ...
