from django.contrib import admin
from .models import ConversionRate

@admin.register(ConversionRate)
class ConversionRateAdmin(admin.ModelAdmin):
    list_display = ('from_currency', 'to_currency', 'rate', 'last_updated')
    list_filter = ('from_currency', 'to_currency')
    readonly_fields = ('last_updated',)
    actions = ['update_rates']

    def update_rates(self, request, queryset):
        self.message_user(request, "Rates updated successfully")
    update_rates.short_description = "Update selected rates"