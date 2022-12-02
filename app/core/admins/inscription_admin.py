from django.contrib import admin


class InscriptionAdmin(admin.ModelAdmin):
    list_display = ('event', 'dorsal', 'car', 'category')
    list_filter = ('event', 'dorsal', 'car', 'category')
    search_fields = ('event__name',)
    raw_id_fields = ('pilot', 'copilot',)
