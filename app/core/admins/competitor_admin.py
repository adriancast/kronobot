from django.contrib import admin
from django.contrib import messages
from django.core.exceptions import MultipleObjectsReturned
from django.utils.safestring import mark_safe
from unfold.admin import ModelAdmin, StackedInline
from core.models import InscriptionModel, CompetitorModel


class PilotInscriptionInline(StackedInline):
    model = InscriptionModel
    fk_name = "pilot"
    extra = 0
    verbose_name = "Pilot inscription"
    readonly_fields = ("car", "category", "dorsal", "event", "copilot")


class CopilotInscriptionInline(StackedInline):
    model = InscriptionModel
    fk_name = "copilot"
    extra = 0
    verbose_name = "Copilot inscription"
    readonly_fields = ("car", "category", "dorsal", "event", "pilot")


@admin.action(description="Set all competitors with same photo")
def set_all_competitors_same_photo(modeladmin, request, queryset):
    try:
        car_photo = queryset.exclude(photo__exact="").get().photo
    except MultipleObjectsReturned:
        messages.error(
            request,
            "Could not set the images for the competitors: You can only select one competitor with image",
        )
        return
    except CompetitorModel.DoesNotExist:
        messages.error(
            request,
            "Could not set the images for the competitors: Any of the selected competitors has an image",
        )
        return

    queryset.update(photo=car_photo)


class CompetitorAdmin(ModelAdmin):
    list_display = ("name", "photo")
    list_filter = ("name",)
    search_fields = ("name",)
    fields = ("name", "photo", "car_photo_preview")
    readonly_fields = ("car_photo_preview",)

    actions = (set_all_competitors_same_photo,)

    def car_photo_preview(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="/mediafiles/{obj.photo}" style="max-height: 100px;" />')

    inlines = (
        PilotInscriptionInline,
        CopilotInscriptionInline,
    )
