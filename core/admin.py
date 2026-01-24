from django.contrib import admin
from .models import User, Property, PropertyImage, RentalApplication, Lease, MaintenanceRequest, Inquiry, Payment

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

@admin.register(RentalApplication)
class RentalApplicationAdmin(admin.ModelAdmin):
    list_display = ('property', 'tenant', 'status', 'application_date')
    list_filter = ('status',)

@admin.register(Lease)
class LeaseAdmin(admin.ModelAdmin):
    list_display = ('property', 'tenant', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active',)

@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'property', 'priority', 'status', 'created_at')
    list_filter = ('status', 'priority')

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('property', 'tenant', 'created_at')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('property', 'owner', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('razorpay_order_id', 'razorpay_payment_id', 'property__title')
    readonly_fields = ('razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature', 'created_at', 'updated_at')