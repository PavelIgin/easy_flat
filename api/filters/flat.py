import datetime
import typing

from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django_filters import rest_framework as filter
from django_filters.widgets import DateRangeWidget
from psycopg2.extras import DateRange

from flat.enums import ArenaTimeLine, OrderByFlat
from flat.models import Flat

from .date_range import CustomDateFromToRangeFilter


class FlatFilter(filter.FilterSet):
    """
    Набор фильтров включающий в cебя
    цена(минимум,максимум)
    Количество комнат(минимум,максимум)
    Квадратура квартиры(минимум,максимум)
    Количество гостей
    Длительность аренды
    Свободна(начальная дата, конечная дата) при помощи метода filter_booked_days
    """

    cost = filter.RangeFilter()
    rooms_count = filter.RangeFilter()
    total_area = filter.RangeFilter()
    max_guest = filter.RangeFilter()
    arena_timeline = filter.ChoiceFilter(choices=ArenaTimeLine.choices)
    booked_days = CustomDateFromToRangeFilter(
        widget=DateRangeWidget(attrs={"placeholder": "%Y-%m-%d"}),
        method="filter_booked_days",
    )
    order_by = filter.ChoiceFilter(
        choices=OrderByFlat.choices, method="filter_order_by"
    )

    def filter_booked_days(
        self,
        queryset: QuerySet,
        name: typing.AnyStr,
        value: typing.List[datetime.date],
    ) -> QuerySet:
        """
        Принимает начальную дату и конечную для выявления
        свободных квартир в этот промежуток времени
        """
        # booked_days принимает начало и конец аренды в формате
        # Пример:{"upper":"2012-12-1","lower":"2012-12-2"}
        ranges = DateRange(value[0], value[1])
        if value[0] > value[1]:
            raise ValidationError("День снятия позже даты сдачи")
        queryset = queryset.exclude(rent__lease_duration__overlap=ranges)
        return queryset

    def filter_order_by(
        self,
        queryset: QuerySet,
        name: typing.AnyStr,
        value: typing.AnyStr,
    ) -> QuerySet:
        if value:
            return queryset.order_by(value)
        return queryset

    class Meta:
        model = Flat
        fields = [
            "cost",
            "rooms_count",
            "total_area",
            "max_guest",
            "arena_timeline",
            "booked_days",
        ]
