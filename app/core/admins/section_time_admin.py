from unfold.admin import ModelAdmin


class SectionTimeAdmin(ModelAdmin):
    list_display = ('section', 'inscription', 'section_time')
    list_filter = ('section', 'inscription', 'section__event__name')
    search_fields = ('section', 'inscription')
