from django.contrib.admin import ModelAdmin
from core import admin
from .models import Stand

class StandAdmin(ModelAdmin):
    list_display = ("name", 'date_render')

# Register your models here.
admin.site.register(Stand, StandAdmin)
