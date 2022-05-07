import typing
from enum import Enum


class BaseEnum(Enum):
    @classmethod
    def choices(cls) -> typing.Generator[typing.Tuple[str, str], None, None]:
        return ((x.value, x.name) for x in cls)
