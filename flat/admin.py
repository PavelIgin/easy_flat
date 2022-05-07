from django.contrib import admin

from .models import Flat, Photo, Renting, SpecialOffer

admin.site.register(Flat)
admin.site.register(Renting)
admin.site.register(Photo)
admin.site.register(SpecialOffer)
