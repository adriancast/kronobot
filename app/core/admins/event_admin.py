from django.contrib import admin
from django.utils.safestring import mark_safe
from unfold.admin import ModelAdmin, TabularInline
from core.models import InscriptionModel


class InscriptionInline(TabularInline):
    model = InscriptionModel
    extra = 0
    can_delete = False
    readonly_fields = ("car", "category", "dorsal", "pilot", "copilot", "car_photo")
    fields = ("dorsal", "pilot", "copilot", "car", "category", "car_photo")
    raw_id_fields = ("pilot", "copilot")

    def car_photo(self, obj):
        if obj.pilot.photo:
            return mark_safe(
                f'<img src="/mediafiles/{obj.pilot.photo}" style="max-height: 100px;" />'
            )


class EventAdmin(ModelAdmin):
    list_display = ("name", "date")
    list_filter = ("name", "date")
    search_fields = ("name", "date")

    inlines = (InscriptionInline,)
