from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
class CommonInfoABC(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        abstract = True


class Record(models.Model):
    title = models.CharField(max_length=255)
    body = models.CharField(max_length=255, blank=True)
    link_to_resource = models.URLField(blank=True, null=True)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)

    tags = models.ManyToManyField("Tag", blank=True, related_name="records")
    status = models.ForeignKey(
        "Status",
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        related_name="records",
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        related_name="records",
    )
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        related_name="records",
        null=True,
        default=None,
    )

    def __str__(self) -> str:
        return self.title


class Category(CommonInfoABC):
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="categories",
    )


class Tag(CommonInfoABC):
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="tags",
    )


class Status(CommonInfoABC):
    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="statuses",
    )
