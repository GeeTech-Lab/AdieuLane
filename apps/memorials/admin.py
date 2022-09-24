from django.contrib import admin
from .models import BurialMemory, MemoryGallery, MemoryTribute


class BurialMemoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'first_name', 'last_name', 'created')
    list_filter = ('user', 'created', 'date_of_death', "cause_of_death")
    search_field = ('first_name', 'last_name')
    prepopulated_fields = {'slug': ('title', 'first_name', 'last_name',)}


admin.site.register(BurialMemory, BurialMemoryAdmin)

admin.site.register(MemoryGallery)

admin.site.register(MemoryTribute)
