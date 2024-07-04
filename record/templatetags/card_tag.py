from django import template


register = template.Library()


@register.inclusion_tag("record/card.html")
def get_record_for_card(record):
    return {"record": record}


@register.inclusion_tag(
    "record/delete_category.html", takes_context=True, name="modal_window"
)
def modal_window_delete(context, cat):
    return {"c": cat}
