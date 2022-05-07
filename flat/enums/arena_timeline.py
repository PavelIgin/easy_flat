from django.utils.translation import gettext_lazy as _

from .base_enum import BaseEnum


class ArenaTimeLine(BaseEnum):
    """
    Выбор краткосрочной или долгосрочной аренды
    """

    OneDay = _("OneDay")
    LongTime = _("LongTime")
