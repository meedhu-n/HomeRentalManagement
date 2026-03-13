from django.contrib import admin
from .models import User, Property, PropertyImage, Payment, Conversation, Message, Wishlist, WebsiteFeedback

# Custom Admin configuration
class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'is_active')
    list_filter = ('role', 'is_active')

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'price', 'status', 'owner')
    list_filter = ('status', 'property_type')
    search_fields = ('title', 'location')
    inlines = [PropertyImageInline]

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('property', 'owner', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('razorpay_order_id', 'razorpay_payment_id', 'property__title')
    readonly_fields = ('razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature', 'created_at', 'updated_at')

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('property', 'tenant', 'owner', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('property__title', 'tenant__username', 'owner__username')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'sender', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('sender__username', 'content')
    readonly_fields = ('created_at',)

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('tenant', 'property', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('tenant__username', 'property__title')
    readonly_fields = ('created_at',)

@admin.register(WebsiteFeedback)
class WebsiteFeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'title', 'is_featured', 'is_approved', 'created_at')
    list_filter = ('rating', 'is_featured', 'is_approved', 'created_at')
    search_fields = ('user__username', 'title', 'comment')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('is_featured', 'is_approved')
