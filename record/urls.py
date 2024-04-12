from django.urls import path

from .views import (
    add_category,
    add_record,
    add_status,
    delete_status,
    index,
    list_categories,
    delete_category,
    list_statuses,
)


urlpatterns = [
    path("", index, name="index"),
    path("addRecord/", add_record, name="add_record"),
    path("addCategory/", add_category, name="add_category"),
    path("addStatus/", add_status, name="add_status"),
    path("listCategories/", list_categories, name="list_categories"),
    path("listStatuses/", list_statuses, name="list_statuses"),
    path("deleteCategory/<int:category_id>", delete_category, name="delete_category"),
    path("deleteStatus/<int:status_id>", delete_status, name="delete_status"),
]
