from django.db import models


class Photo(models.Model):
    photo = models.ImageField(upload_to="flat_images", null=True, blank=True)
    flat = models.ForeignKey("Flat", on_delete=models.CASCADE)
