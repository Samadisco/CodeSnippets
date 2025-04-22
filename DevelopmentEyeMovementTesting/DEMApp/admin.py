from django.contrib import admin

# Register your models here.
from .models import *
class RenderingTestData(admin.ModelAdmin):
    list_display = [field.name for field in TestData._meta.get_fields()]

class RenderingPxData(admin.ModelAdmin):
    list_display = [field.name for field in PxData._meta.get_fields()]

admin.site.register(TestData, RenderingTestData)
admin.site.register(PxData, RenderingPxData)