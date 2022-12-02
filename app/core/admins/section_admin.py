from django.contrib import admin


class SectionAdmin(admin.ModelAdmin):
    list_display = ('event', 'name', 'code',)
    list_filter = ('event', 'name', 'code',)
    search_fields = ('event__name', 'name', 'code',)