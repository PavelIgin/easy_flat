import typing

from django.contrib.postgres.fields import DateRangeField
from django.core.exceptions import ValidationError
from django.db import models

from .special_offer import SpecialOffer


class Renting(models.Model):
    """
    Сущность бронировки квартиры
    """

    flat = models.ForeignKey("Flat", on_delete=models.CASCADE, related_name="rent", verbose_name="Апартаменты")
    user = models.ForeignKey("user.CustomUser", on_delete=models.CASCADE, verbose_name='Съемщик')
    count_guest = models.PositiveIntegerField(verbose_name='Кол-во гостей')
    lease_duration = DateRangeField(verbose_name='')
    # TODO переименовать lease_duration в lease_range
    cost_of_rent = models.PositiveBigIntegerField(null=True, blank=True, default=0)
    # TODO пересоздать модель, сделать поле cost_of_rent обязательным ненулевым

    def clean(self) -> None:
        if (
            Renting.objects.filter(
                user=self.user, lease_duration__overlap=self.lease_duration
            )
            .exclude(id=self.id)
            .exists()
        ):
            raise ValidationError(
                "У вас уже есть забронированная квартира в этот период"
            )
        if self.count_guest > self.flat.max_guest:
            raise ValidationError("Слишком много гостей")
        is_booked = (
            self.flat.rent.filter(lease_duration__overlap=self.lease_duration)
            .exclude(id=self.id)
            .exists()
        )
        if is_booked:
            raise ValidationError("Квартира занята")

    def save(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        self.clean()
        self.cost_of_rent = self.get_cost_of_rent()
        super().save()

    def get_cost_of_rent(self):
        """
        Метод расчитывает стоимость аренды с учетом специальных предложений от арендодателя
        """
        offers = SpecialOffer.objects.filter(flat=self.flat, date__overlap=self.lease_duration)
        lease_start, lease_end = self.lease_duration._lower, self.lease_duration._upper
        lease = self.lease_duration._upper - self.lease_duration._lower

        cost_of_rent = 0
        for offer in offers:
            offer_start, offer_end = offer.date._lower, offer.date._upper
            offer_is_active = lease_start > offer_start
            if offer_is_active:
                leas_low_offer = offer_end - lease_start
                cost_of_rent += leas_low_offer.days * offer.cost
                lease -= leas_low_offer
            elif lease_end < offer_end:
                leas_high_offer = lease_end - offer_start
                cost_of_rent += leas_high_offer.days * offer.cost
                lease -= leas_high_offer
            else:
                leas_offer = offer_end - offer_start
                cost_of_rent += leas_offer.days * offer.cost
                lease -= leas_offer
        cost_of_rent += self.flat.cost * lease.days
        return cost_of_rent

    def get_cost_of_rent_draft(self):
        """
        Метод расчитывает стоимость аренды с учетом специальных предложений от арендодателя
        """
        '''
        Есть стартовая цена, которая работает, если нет вообще никаких офферов
        
        1000
        1000
        1000
        ...
        1000
        ___
        высчитываем, как меняется цена с учетом офферов
        
        оффер 2 - +7%

        
        '''