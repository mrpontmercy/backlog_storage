from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import NameForm, RecordForm

from unidecode import unidecode
from django.template.defaultfilters import slugify

from .models import Category, Record, Status

# Create your views here.


def index(request: HttpRequest):
    user = request.user
    if user.is_authenticated and user.pk:
        records = (
            Record.objects.filter(author_id=user.pk)
            .prefetch_related("tags")
            .select_related("category", "status")
        )
    else:
        records = []
    # records = list(RecordDAO().fetch_all(Record))
    context = {
        "records": records,
        "title": "Главная",
    }
    return render(request, "record/index.html", context=context)


@login_required(login_url="users:login")
def add_category(request: HttpRequest):
    if request.method == "POST":
        form = NameForm(request.POST)

        if form.is_valid():
            c = form.save(commit=False)
            c.author = request.user
            c.slug = slugify(unidecode(c.name) + "_" + c.author.username)
            try:
                c.save()
            except IntegrityError:
                messages.add_message(
                    request, messages.INFO, "Не удалось сохранить данную категорию"
                )

            return redirect("list_categories")
    else:
        form = NameForm()

    context = {
        "title": "Добавить категорию",
        "form": form,
    }
    return render(request, "record/add_category.html", context=context)


@login_required(login_url="users:login")
def add_record(request: HttpRequest):
    if request.method == "POST":
        form = RecordForm(request.POST, request=request)
        if form.is_valid():
            r = form.save(commit=False)
            r.author = request.user
            r.save()
            return redirect("index")
    else:
        form = RecordForm(request=request)

    context = {"title": "Добавление новой записи", "form": form}

    return render(request, "record/addrecord.html", context=context)


@login_required(login_url="users:login")
def list_categories(request: HttpRequest):
    categories = Category.objects.filter(author=request.user)
    context = {
        "title": "Категории",
        "categories": categories,
    }
    return render(request, "record/list_categories.html", context=context)


@login_required(login_url="users:login")
def delete_category(request: HttpRequest, category_id: int):
    obj_string = "категорию"
    cat = get_object_or_404(Category, id=category_id, author_id=request.user.id)  # type: ignore
    context = {
        "obj": cat,
        "obj_string": obj_string,
        "link_back_page": reverse("list_categories"),
    }
    if request.method == "POST":
        cat.delete()
        return redirect("list_categories")

    return render(request, "record/delete_obj.html", context=context)


@login_required(login_url="users:login")
def list_statuses(request: HttpRequest):
    statuses = Status.objects.filter(author=request.user)
    context = {
        "title": "Статусы",
        "statuses": statuses,
    }
    return render(request, "record/list_statuses.html", context=context)


@login_required(login_url="users:login")
def add_status(request: HttpRequest):
    if request.method == "POST":
        form = NameForm(request.POST, instance=Status())

        if form.is_valid():
            c = form.save(commit=False)
            c.author = request.user
            c.slug = slugify(unidecode(c.name) + "_" + c.author.username)  # type: ignore
            try:
                c.save()
            except IntegrityError:
                messages.add_message(
                    request, messages.INFO, "Не удалось сохранить данную категорию"
                )

            return redirect("list_statuses")
    else:
        form = NameForm(instance=Status())

    context = {
        "title": "Добавить статус",
        "form": form,
    }
    return render(request, "record/add_status.html", context=context)


@login_required(login_url="users:login")
def delete_status(request: HttpRequest, status_id: int):
    obj_string = "статус"
    cat = get_object_or_404(Status, id=category_id, author_id=request.user.id)  # type: ignore
    context = {
        "obj": cat,
        "obj_string": obj_string,
        "link_back_page": reverse("list_categories"),
    }
    if request.method == "POST":
        cat.delete()
        return redirect("list_statuses")

    return render(request, "record/delete_obj.html", context=context)
