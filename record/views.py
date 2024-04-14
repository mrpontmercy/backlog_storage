from django.contrib.auth.decorators import login_required
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from record.services.common_funcs import add_row_with_slug_to_db

from .forms import RecordForm


from .models import Category, Record, Status, Tag

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
    context = {
        "records": records,
        "title": "Главная",
    }
    return render(request, "record/index.html", context=context)


@login_required(login_url="users:login")
def add_category(request: HttpRequest):
    form, ok = add_row_with_slug_to_db(
        request,
        Category(),
    )
    if ok:
        return redirect("list_categories")

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
            form.save_m2m()  # For m2m relationships, we first save a record and then save the relationship.
            return redirect("index")
    else:
        form = RecordForm(request=request)

    context = {"title": "Добавление новой записи", "form": form}

    return render(request, "record/addrecord.html", context=context)


@login_required(login_url="users:login")
def delete_record(request: HttpRequest, record_id: int):
    obj_string = "запись"
    obj = get_object_or_404(Record, id=record_id, author=request.user)
    print(obj.title)
    context = {
        "title": "Удалить",
        "obj": obj,
        "obj_string": obj_string,
        "link_back_page": reverse("index"),
        "delete_view": reverse("delete_record", kwargs={"record_id": record_id}),
    }
    if request.method == "POST":
        obj.delete()
        return redirect("index")

    return render(request, "record/delete_obj.html", context=context)


@login_required(login_url="users:login")
def edit_record(request: HttpRequest, record_id: int):
    rec = get_object_or_404(Record, id=record_id, author=request.user)
    form = RecordForm(request.POST or None, instance=rec, request=request)
    if form.is_valid():
        rec = form.save(commit=False)
        rec.save()
        form.save_m2m()
        return redirect("index")

    context = {
        "title": "Изменение записи",
        "form": form,
        "link_back_page": reverse("index"),
    }

    return render(request, "record/edit_record.html", context=context)


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
    obj = get_object_or_404(Category, id=category_id, author_id=request.user.id)  # type: ignore
    context = {
        "obj": obj,
        "obj_string": obj_string,
        "link_back_page": reverse("list_categories"),
        "delete_view": reverse("delete_category", kwargs={"category_id": obj.id}),
    }
    if request.method == "POST":
        obj.delete()
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
    form, ok = add_row_with_slug_to_db(
        request,
        Status(),
    )
    if ok:
        return redirect("list_statuses")

    context = {
        "title": "Добавить статус",
        "form": form,
    }
    return render(request, "record/add_status.html", context=context)


@login_required(login_url="users:login")
def delete_status(request: HttpRequest, status_id: int):
    obj_string = "статус"
    obj = get_object_or_404(Status, id=status_id, author_id=request.user.id)  # type: ignore

    if request.method == "POST":
        obj.delete()
        return redirect("list_statuses")

    context = {
        "obj": obj,
        "obj_string": obj_string,
        "link_back_page": reverse("list_statuses"),
        "delete_view": reverse("delete_status", kwargs={"status_id": obj.id}),
    }
    return render(request, "record/delete_obj.html", context=context)


@login_required(login_url="users:login")
def list_tags(request: HttpRequest):
    tags = Tag.objects.filter(author=request.user)

    print(tags)
    context = {
        "title": "Тэги",
        "tags": tags,
    }

    return render(request, "record/list_tags.html", context=context)


@login_required(login_url="users:login")
def add_tag(request: HttpRequest):
    form, ok = add_row_with_slug_to_db(
        request,
        Tag(),
    )
    if ok:
        return redirect("list_tags")

    context = {
        "title": "Добавить Тэг",
        "form": form,
    }
    return render(request, "record/add_tag.html", context=context)


@login_required(login_url="users:login")
def delete_tag(request: HttpRequest, tag_id: int):
    obj_string = "тэг"
    obj = get_object_or_404(Tag, id=tag_id, author_id=request.user.id)  # type: ignore

    if request.method == "POST":
        obj.delete()
        return redirect("list_tags")

    context = {
        "obj": obj,
        "obj_string": obj_string,
        "link_back_page": reverse("list_tags"),
        "delete_view": reverse("delete_tag", kwargs={"tag_id": obj.id}),
    }
    return render(request, "record/delete_obj.html", context=context)
