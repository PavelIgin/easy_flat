from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from flat.enums import RentTimeLine


class Flat(models.Model):
    """
    Модель квартиры имеет краткосрочную сдачу или для помесячной сдачи
    """

    owner = models.ForeignKey("user.CustomUser", on_delete=models.CASCADE, null=True)
    rooms_count = models.SmallIntegerField()
    cost = models.PositiveIntegerField()

    comfortable = models.CharField(max_length=200, null=True, blank=True, verbose_name='Список удобств кратко')

    max_guest = models.SmallIntegerField()
    arena_timeline = models.CharField(choices=RentTimeLine.choices(), max_length=200,
                                      verbose_name='Длительность съема')
    total_area = models.SmallIntegerField(verbose_name='Жилая площадь')
    date_publish = models.DateTimeField(auto_now=True)
    avg_rating = models.FloatField(default=0, null=True)

    rating = GenericRelation("community.rating", null=True, blank=True)
