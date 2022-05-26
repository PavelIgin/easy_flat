from __future__ import absolute_import, unicode_literals

import datetime

from django.utils.timezone import now, timedelta

from flat.models import Renting

from celery.task import periodic_task

from yookassa import Payment


@periodic_task(run_every=(timedelta(seconds=15)), name='check_pay')
def check_pay():
    rents = Renting.objects.filter(is_payed=False)
    for rent in rents:
        payment = Payment.find_one(payment_id=rent.id_payment)
        date = datetime.datetime.strptime(payment.created_at, "%Y-%m-%dT%H:%M:%S.%f%z")
        print(payment.paid)

        if date + timedelta(minutes=15) < now():
            rent.delete()
            continue
        if payment.paid:
            rent.is_payed: bool = payment.paid
            rent.save()
