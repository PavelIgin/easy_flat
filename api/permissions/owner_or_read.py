from django.db.models import Model
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView

from community.models import Rating
from flat.models import Flat, Renting, SpecialOffer
from user.models import CustomUser


class OwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(
        self, request: Request, view: APIView, obj: Model
    ) -> bool:
        is_safe_method = request.method in permissions.SAFE_METHODS
        if isinstance(obj, Flat):
            #Возможность редактировать Flat только собственнику
            return bool(is_safe_method or request.user == obj.owner)
        if isinstance(obj, Renting):
            #Возможность редактировать Renting только собственнику
            return bool(is_safe_method or request.user == obj.user)
        if isinstance(obj, Rating):
            #Возможность редактировать Rating только собственнику
            return bool(is_safe_method or request.user == obj.user)
        if isinstance(obj, SpecialOffer):
            #Возможнось редактировать SpecialOffer только собственнику
            return bool(is_safe_method or request.user == obj.flat.owner)
            return is_safe_method or request.user == obj.owner
        if isinstance(obj, (Renting, Rating)):
            return is_safe_method or request.user == obj.user
        if isinstance(obj, CustomUser):
            return is_safe_method or request.user == obj
