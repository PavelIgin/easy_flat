from django.utils.translation import gettext_lazy as _

from .base_enum import BaseEnum


class OrderByFlat(BaseEnum):
    """
    Выбор сортировки квартир
    """

    IncreaseCost = _("cost")
    DescendingCost = _("-cost")
    IncreaseRoomsCount = _("rooms_count")
    DescendingCostRoomsCount = _("-rooms_count")
    IncreaseTotalArea = _("total_area")
    DescendingTotalArea = _("-total_area")
    IncreaseMaxGuest = _("max_guest")
    DescendingMaxGuest = _("-max_guest")
