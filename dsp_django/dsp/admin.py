from django.contrib import admin
from .models import Campaign, Strategy, Creative

# Register your models here.

admin.site.register(Campaign)
admin.site.register(Strategy)
# admin.site.register(Creative)


# Register the Admin classes for Creative using the decorator
@admin.register(Creative)
class CreativeAdmin(admin.ModelAdmin):
    list_filter = ('campaign', 'strategies', 'status',)
    list_display = ('name', 'campaign', 'status', 'target_url', 'inventory_type',)
