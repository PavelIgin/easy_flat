from django.contrib import admin

from user.models import CustomUser, PasswordChangeOrder, SignUpOrder

admin.site.register(SignUpOrder)
admin.site.register(CustomUser)
admin.site.register(PasswordChangeOrder)

# Register your models here.
