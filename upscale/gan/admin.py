from django.contrib import admin
from .models import scaled
# Register your models here.

class imageAdmin(admin.ModelAdmin):
    readonly_fields=("id",)

admin.site.register(scaled,imageAdmin)
