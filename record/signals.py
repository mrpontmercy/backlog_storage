from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from record.models import Status


@receiver(post_save, sender=User)
def create_basic_user_tags_after_registration(sender, instance, created, **kwargs):
    if created:
        s1 = Status(name="Начат", author=instance)
        s2 = Status(name="Обработан", author=instance)
        s3 = Status(name="Не закончен", author=instance)
        s4 = Status(name="Бэклог", author=instance)

        try:
            s1.save()
            s2.save()
            s3.save()
            s4.save()
        except IntegrityError:
            transaction.rollback()
