from django import template
from django.db.models import Model
from django.db.models.base import ModelBase

from record.models import Category

register = template.Library()


@register.inclusion_tag("record/card.html")
def get_record_for_card(record):
    return {"record": record}


@register.inclusion_tag(
    "record/delete_category.html", takes_context=True, name="modal_window"
)
def modal_window_delete(context, cat):
    return {"c": cat}
