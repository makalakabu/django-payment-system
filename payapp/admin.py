from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import UserProfile, Transaction

User = get_user_model()

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_email', 'currency', 'balance', 'is_active_user')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    list_filter = ('currency',)
    list_select_related = ('user',)
    
    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'
    get_username.admin_order_field = 'user__username'
    
    def get_email(self, obj):
        return obj.user.email or "Not set"
    get_email.short_description = 'Email'
    get_email.admin_order_field = 'user__email'
    
    def is_active_user(self, obj):
        return obj.user.is_active
    is_active_user.short_description = 'Active'
    is_active_user.boolean = True
    is_active_user.admin_order_field = 'user__is_active'

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'get_sender',
        'get_recipient',
        'get_amount',
        'currency',
        'transaction_type',
        'status',
        'created_at'
    )
    list_filter = ('transaction_type', 'status', 'currency', 'created_at')
    search_fields = (
        'sender__username',
        'sender__email',
        'recipient__username',
        'recipient__email',
        'description'
    )
    date_hierarchy = 'created_at'
    list_select_related = ('sender', 'recipient')
    
    def get_sender(self, obj):
        return f"{obj.sender.username} ({obj.sender.email})" if obj.sender.email else obj.sender.username
    get_sender.short_description = 'Sender'
    get_sender.admin_order_field = 'sender__email'
    
    def get_recipient(self, obj):
        return f"{obj.recipient.username} ({obj.recipient.email})" if obj.recipient.email else obj.recipient.username
    get_recipient.short_description = 'Recipient'
    get_recipient.admin_order_field = 'recipient__email'
    
    def get_amount(self, obj):
        return f"{obj.amount} {obj.currency}"
    get_amount.short_description = 'Amount'
    get_amount.admin_order_field = 'amount'

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_editable = ('email', 'first_name', 'last_name') 
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    actions = ['fix_empty_emails']
    
    def fix_empty_emails(self, request, queryset):
        updated_count = 0
        for user in queryset.filter(email=''):
            user.email = f"{user.username}@example.com"
            user.save()
            updated_count += 1
        self.message_user(request, f"Fixed {updated_count} empty emails")
    fix_empty_emails.short_description = "Fix empty emails"


if admin.site.is_registered(User):
    admin.site.unregister(User)


admin.site.register(User, UserAdmin)