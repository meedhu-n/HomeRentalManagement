from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# 1. Custom User Model
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        OWNER = "OWNER", "Owner"
        TENANT = "TENANT", "Tenant"

    email = models.EmailField(unique=True, null=False, blank=False) 
    role = models.CharField(max_length=50, choices=Role.choices, default=Role.TENANT)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

# 2. Property Model
class Property(models.Model):
    class Status(models.TextChoices):
        PENDING_APPROVAL = "PENDING", "Pending Approval"
        AVAILABLE = "AVAILABLE", "Available"
        RENTED = "RENTED", "Rented"
        MAINTENANCE = "MAINTENANCE", "Maintenance"

    class Furnishing(models.TextChoices):
        UNFURNISHED = "UNFURNISHED", "Unfurnished"
        SEMI_FURNISHED = "SEMI_FURNISHED", "Semi-Furnished"
        FULLY_FURNISHED = "FULLY_FURNISHED", "Fully Furnished"

    class Facing(models.TextChoices):
        NORTH = "NORTH", "North"
        SOUTH = "SOUTH", "South"
        EAST = "EAST", "East"
        WEST = "WEST", "West"
        NORTHEAST = "NORTHEAST", "North-East"
        NORTHWEST = "NORTHWEST", "North-West"
        SOUTHEAST = "SOUTHEAST", "South-East"
        SOUTHWEST = "SOUTHWEST", "South-West"

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    title = models.CharField(max_length=255)
    ad_title = models.CharField(max_length=255, blank=True, null=True, help_text="Short ad title")
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    property_type = models.CharField(max_length=100)
    bhk = models.IntegerField(default=1, help_text="Number of BHKs (Bedrooms)")
    bathrooms = models.IntegerField(default=1, help_text="Number of bathrooms")
    furnishing = models.CharField(max_length=50, choices=Furnishing.choices, default=Furnishing.SEMI_FURNISHED)
    super_built_area = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Super built area in sqft")
    bachelors_allowed = models.BooleanField(default=True, help_text="Are bachelors allowed?")
    total_floors = models.IntegerField(default=1, help_text="Total floors in the building")
    facing = models.CharField(max_length=50, choices=Facing.choices, default=Facing.NORTH)
    built_year = models.IntegerField(blank=True, null=True, help_text="Year the property was built")
    amenities = models.TextField(help_text="Comma-separated list of amenities", blank=True)
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.PENDING_APPROVAL)
    # Added is_paid field
    is_paid = models.BooleanField(default=False)
    # Plan-related fields
    plan_type = models.CharField(max_length=20, choices=[
        ('basic', 'Basic Plan'),
        ('standard', 'Standard Plan'),
        ('premium', 'Premium Plan')
    ], default='basic', help_text="Selected plan type")
    plan_expiry_date = models.DateTimeField(blank=True, null=True, help_text="Date when the plan expires")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Properties"

    def __str__(self):
        return self.title

    def is_plan_active(self):
        """Check if the property plan is still active"""
        from django.utils import timezone
        if self.plan_expiry_date:
            return timezone.now() < self.plan_expiry_date
        return False

    def days_remaining(self):
        """Get the number of days remaining in the plan"""
        from django.utils import timezone
        if self.plan_expiry_date:
            delta = self.plan_expiry_date - timezone.now()
            return max(0, delta.days)
        return 0

# ... (Rest of the file remains the same: PropertyImage, RentalApplication, Lease, MaintenanceRequest, Inquiry) ...
class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/')
    
    def __str__(self):
        return f"Image for {self.property.title}"

class RentalApplication(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"

    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='applications')
    application_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    message = models.TextField(blank=True)
    
    def __str__(self):
        return f"Application by {self.tenant.username} for {self.property.title}"

class Lease(models.Model):
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leases')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='leases')
    start_date = models.DateField()
    end_date = models.DateField()
    monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
    document = models.FileField(upload_to='leases/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Lease: {self.property.title} - {self.tenant.username}"

class MaintenanceRequest(models.Model):
    class Priority(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"
        EMERGENCY = "EMERGENCY", "Emergency"

    class Status(models.TextChoices):
        OPEN = "OPEN", "Open"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        RESOLVED = "RESOLVED", "Resolved"

    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='maintenance_requests')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='maintenance_requests')
    title = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.MEDIUM)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    image = models.ImageField(upload_to='maintenance/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.priority} - {self.title}"

class Inquiry(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='inquiries')
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_inquiries')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Inquiries"

    def __str__(self):
        return f"Inquiry from {self.tenant.username} for {self.property.title}"

# 3. Payment Model for Property Registration Fee
class Payment(models.Model):
    class PaymentStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        SUCCESS = "SUCCESS", "Success"
        FAILED = "FAILED", "Failed"
    
    property = models.OneToOneField(Property, on_delete=models.CASCADE, related_name='payment')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    razorpay_order_id = models.CharField(max_length=255, unique=True)
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount in INR
    status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment for {self.property.title} - {self.status}"

# Messaging System
class Conversation(models.Model):
    """Conversation between a tenant and owner about a property"""
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='conversations')
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tenant_conversations')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('property', 'tenant', 'owner')
        ordering = ['-updated_at']

    def __str__(self):
        return f"Conversation: {self.tenant.username} - {self.owner.username} about {self.property.title}"

    def get_last_message(self):
        return self.messages.last()

class Message(models.Model):
    """Individual message in a conversation"""
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Message from {self.sender.username} at {self.created_at}"

# Review System
class Review(models.Model):
    """Reviews for properties by tenants and owners"""
    class Rating(models.IntegerChoices):
        ONE = 1, "1 Star"
        TWO = 2, "2 Stars"
        THREE = 3, "3 Stars"
        FOUR = 4, "4 Stars"
        FIVE = 5, "5 Stars"

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    rating = models.IntegerField(choices=Rating.choices)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('property', 'reviewer')  # One review per user per property

    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.property.title} - {self.rating} stars"

# Wishlist System
class Wishlist(models.Model):
    """Wishlist for tenants to save favorite properties"""
    tenant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist_items')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='wishlisted_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('tenant', 'property')  # One wishlist entry per tenant per property

    def __str__(self):
        return f"{self.tenant.username}'s wishlist - {self.property.title}"
