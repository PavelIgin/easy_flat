import typing
import uuid

from django.contrib.postgres.fields import DateRangeField
from django.core.exceptions import ValidationError
from django.db import models

from .flat import Flat

from yookassa import Payment


class Renting(models.Model):
    """
    Сущность бронировки квартиры
    """

    flat = models.ForeignKey("Flat", on_delete=models.CASCADE, related_name="rent")
    user = models.ForeignKey("user.CustomUser", on_delete=models.CASCADE)
    count_guest = models.PositiveIntegerField()
    lease_duration = DateRangeField()
    cost_of_rent = models.PositiveBigIntegerField(null=True, blank=True, default=0)
    is_payed = models.BooleanField(default=False)
    id_payment = models.CharField(max_length=200)

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
        if self.id_payment is '':
            self.create_payments()
        super().save()

    def get_cost_of_rent(self):
        """
        Метод расчитывает стоимость аренды с учетом специальных предложений от арендодателя
        """
        flat = Flat.objects.get(id=self.flat.id)
        offers = flat.special_offer.filter(date__overlap=self.lease_duration)

        leas = self.lease_duration._upper-self.lease_duration._lower
        cost_of_rent = 0
        for offer in offers:
            if self.lease_duration._lower > offer.date._lower:
                leas_low_offer = offer.date._upper-self.lease_duration._lower
                cost_of_rent += leas_low_offer.days * offer.cost
                leas -= leas_low_offer
            elif self.lease_duration._upper < offer.date._upper:
                leas_high_offer = self.lease_duration._upper-offer.date._lower
                cost_of_rent += leas_high_offer.days * offer.cost
                leas -= leas_high_offer
            else:
                leas_offer = offer.date._upper - offer.date._lower
                cost_of_rent += leas_offer.days * offer.cost
                leas -= leas_offer
        cost_of_rent += self.flat.cost * leas.days
        return cost_of_rent

    def create_payments(self):
        uuid4 = uuid.uuid4()
        payment = Payment.create({
            "amount": {
                "value": f"{self.cost_of_rent}",
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "example.com"
            },
            "capture": True,
            "description": f"Аренда  {self.flat}"
        }, uuid4)
        self.is_payed = payment.paid
        self.id_payment = payment.id
