
from django.contrib import admin
from .models import RegistrationRequest

@admin.register(RegistrationRequest)
class RegistrationRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_email', 'approved', 'created_at')
    list_filter = ('approved', 'created_at')
    search_fields = ('user__username', 'user__email')
    actions = ['approve_requests']
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'
    user_email.admin_order_field = 'user__email'
    
    def approve_requests(self, request, queryset):
        queryset.update(approved=True)
        self.message_user(request, f"{queryset.count()} registration requests approved")
    approve_requests.short_description = "Approve selected requests"