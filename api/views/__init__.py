from .change_password import PasswordChangeOrderViewSet
from .create_user import CreateUserViewSet
from .flat import FlatViewSet
from .rating import RatingViewSet
from .rent import RentingViewSet
from .user import CustomUserViewSet

__all__ = [
    "PasswordChangeOrderViewSet",
    "CreateUserViewSet",
    "FlatViewSet",
    "RatingViewSet",
    "RentingViewSet",
    "CustomUserViewSet",
]
