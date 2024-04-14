from django.urls import path

from .views import (
    add_category,
    add_record,
    add_status,
    add_tag,
    delete_record,
    delete_status,
    delete_tag,
    edit_record,
    index,
    list_categories,
    delete_category,
    list_statuses,
    list_tags,
)


urlpatterns = [
    path("", index, name="index"),
    path("addRecord/", add_record, name="add_record"),
    path("editRecord/<int:record_id>", edit_record, name="edit_record"),
    path("addCategory/", add_category, name="add_category"),
    path("addStatus/", add_status, name="add_status"),
    path("addTag/", add_tag, name="add_tag"),
    path("listCategories/", list_categories, name="list_categories"),
    path("listStatuses/", list_statuses, name="list_statuses"),
    path("listTags/", list_tags, name="list_tags"),
    path("deleteCategory/<int:category_id>", delete_category, name="delete_category"),
    path("deleteStatus/<int:status_id>", delete_status, name="delete_status"),
    path("deleteTag/<int:tag_id>", delete_tag, name="delete_tag"),
    path("deleteRecord/<int:record_id>", delete_record, name="delete_record"),
]
