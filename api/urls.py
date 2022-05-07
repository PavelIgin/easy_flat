"""easy_flat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from rest_framework import routers

from api.views import CustomUserViewSet, FlatViewSet, RatingViewSet, RentingViewSet

router = routers.DefaultRouter()

router.register("flat", FlatViewSet, basename="flat")
router.register("rent", RentingViewSet, basename="rent")
router.register("rating", RatingViewSet, basename="rating")
router.register("user", CustomUserViewSet, basename="user")
urlpatterns = [] + router.urls
