from django.db import models
from django.contrib.postgres.fields import DateRangeField
from django.core.exceptions import ValidationError

from flat.messages import SPECIAL_OFFER_ALREADY_EXIST


class SpecialOffer(models.Model):
    """
    Модель специальных предложения для выставки специальной стоимости в некоторые дни
    """
    flat = models.ForeignKey('Flat', on_delete=models.CASCADE)
    date = DateRangeField()
    cost = models.PositiveBigIntegerField()

    def clean(self):
        coincidences = SpecialOffer.objects.filter(date__overlap=self.date, flat=self.flat).exclude(id=self.id)
        if coincidences:
            raise ValidationError(SPECIAL_OFFER_ALREADY_EXIST)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.clean()
        super().save()
