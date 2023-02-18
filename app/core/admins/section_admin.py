from unfold.admin import ModelAdmin

class SectionAdmin(ModelAdmin):
    list_display = ('event', 'name', 'code',)
    list_filter = ('event', 'name', 'code',)
    search_fields = ('event__name', 'name', 'code',)