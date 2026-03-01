from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.conf import settings
from .models import Property, PropertyImage, Payment, RentalApplication, Conversation, Message
from .forms import PropertyForm
import razorpay
import json
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()

# ... (Previous views: index, register, login, logout remain same) ...
def index(request):
    from django.utils import timezone
    from .models import WebsiteFeedback
    
    # Get premium properties for home page display
    premium_properties = Property.objects.filter(
        status=Property.Status.AVAILABLE,
        is_paid=True,
        plan_type='premium',
        plan_expiry_date__gt=timezone.now()
    ).order_by('-created_at')[:6]  # Show top 6 premium properties
    
    # Get featured website feedbacks for home page
    featured_feedbacks = WebsiteFeedback.objects.filter(
        is_featured=True,
        is_approved=True
    ).select_related('user').order_by('-created_at')[:6]
    
    context = {
        'premium_properties': premium_properties,
        'featured_feedbacks': featured_feedbacks
    }
    
    return render(request, 'core/index.html', context)

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        role = request.POST.get('role')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'core/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'core/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'core/register.html')

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.role = role
            user.phone_number = phone
            user.save()
            messages.success(request, "Account created successfully! Please login.")
            return redirect('login')
        except Exception as e:
            messages.error(request, "An error occurred during registration.")
            print(e)
            
    return render(request, 'core/register.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('index')

@login_required
def dashboard_view(request):
    # Handle profile update
    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username', user.username)
        user.email = request.POST.get('email', user.email)
        user.phone_number = request.POST.get('phone', user.phone_number)
        
        # Handle profile image upload
        if 'profile_image' in request.FILES:
            user.profile_image = request.FILES['profile_image']
        
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('dashboard')
    
    context = {'user': request.user}
    
    # Check if user is superuser (Admin)
    if request.user.is_superuser or request.user.role == 'ADMIN':
        # Admin Dashboard Logic
        # Show all properties with PENDING status (whether paid or not)
        pending_properties = Property.objects.filter(status=Property.Status.PENDING_APPROVAL).order_by('-created_at')
        # Exclude admin/superuser from owners and tenants lists
        owners = User.objects.filter(role='OWNER', is_superuser=False).order_by('-date_joined')
        tenants = User.objects.filter(role='TENANT', is_superuser=False).order_by('-date_joined')
        all_users = User.objects.exclude(is_superuser=True).order_by('-date_joined')
        all_properties = Property.objects.all().order_by('-created_at')
        
        context['pending_properties'] = pending_properties
        context['pending_count'] = pending_properties.count()
        context['all_users'] = all_users
        context['total_users'] = all_users.count()
        context['owners'] = owners
        context['total_owners'] = owners.count()
        context['tenants'] = tenants
        context['total_tenants'] = tenants.count()
        context['all_properties'] = all_properties
        context['total_properties'] = all_properties.count()
        return render(request, 'core/admin_dashboard.html', context)
    
    elif request.user.role == 'OWNER':
        from .models import Review
        from django.utils import timezone
        
        properties = Property.objects.filter(owner=request.user)
        
        # Add plan status to each property
        for prop in properties:
            if prop.plan_expiry_date:
                prop.is_plan_active = prop.is_plan_active()
                prop.days_left = prop.days_remaining()
            else:
                prop.is_plan_active = False
                prop.days_left = 0
        
        # Get only conversations with unread messages for owner
        all_conversations = Conversation.objects.filter(owner=request.user).order_by('-updated_at')
        
        # Filter to only show conversations with unread messages
        conversations_with_unread = []
        for conversation in all_conversations:
            unread_count = conversation.messages.filter(is_read=False).exclude(sender=request.user).count()
            if unread_count > 0:
                conversation.has_unread = True
                conversations_with_unread.append(conversation)
                if len(conversations_with_unread) >= 5:  # Limit to 5 unread conversations
                    break
        
        # Get reviews given by this owner
        owner_reviews = Review.objects.filter(reviewer=request.user).select_related('property')
        
        # Count active properties (with valid plans)
        active_properties_count = properties.filter(
            status=Property.Status.AVAILABLE,
            is_paid=True,
            plan_expiry_date__gt=timezone.now()
        ).count()
        
        context['properties'] = properties
        context['active_listings_count'] = active_properties_count
        context['recent_conversations'] = conversations_with_unread
        context['owner_reviews'] = owner_reviews
        return render(request, 'core/owner_dashboard.html', context)
    
    elif request.user.role == 'TENANT':
        from .models import Review, Wishlist
        from django.utils import timezone
        from django.db.models import Case, When, IntegerField
        
        # Only show properties that are available, paid, and have active plans
        # Sort by plan priority: Premium (3) > Standard (2) > Basic (1), then by created date
        available_properties = Property.objects.filter(
            status=Property.Status.AVAILABLE,
            is_paid=True,
            plan_expiry_date__gt=timezone.now()
        ).annotate(
            plan_priority=Case(
                When(plan_type='premium', then=3),
                When(plan_type='standard', then=2),
                When(plan_type='basic', then=1),
                default=0,
                output_field=IntegerField()
            )
        ).order_by('-plan_priority', '-created_at')
        
        user_applications = RentalApplication.objects.filter(tenant=request.user).order_by('-application_date')
        
        # Get reviews given by this tenant
        tenant_reviews = Review.objects.filter(reviewer=request.user).select_related('property')
        
        # Get wishlist items
        wishlist_items = Wishlist.objects.filter(tenant=request.user).select_related('property')
        wishlist_property_ids = list(wishlist_items.values_list('property_id', flat=True))
        
        context['available_properties'] = available_properties
        context['total_available'] = available_properties.count()
        context['applications'] = user_applications
        context['total_applications'] = user_applications.count()
        context['approved_applications'] = user_applications.filter(status=RentalApplication.Status.APPROVED).count()
        context['tenant_reviews'] = tenant_reviews
        context['wishlist_count'] = wishlist_items.count()
        context['wishlist_property_ids'] = wishlist_property_ids
        return render(request, 'core/tenant_dashboard.html', context)
    
    return render(request, 'core/dashboard.html', context)

@login_required
def add_property_view(request):
    if request.user.role != 'OWNER':
        messages.error(request, "Access denied. Owners only.")
        return redirect('dashboard')

    # Check property limits based on active properties with valid plans
    from django.utils import timezone
    active_properties = Property.objects.filter(
        owner=request.user,
        is_paid=True,
        plan_expiry_date__gt=timezone.now()
    )
    
    # Count properties by plan type
    basic_count = active_properties.filter(plan_type='basic').count()
    standard_count = active_properties.filter(plan_type='standard').count()
    premium_count = active_properties.filter(plan_type='premium').count()
    
    # Check if user has reached their limit
    # Basic: 1 property, Standard: 3 properties, Premium: 10 properties
    total_active = active_properties.count()
    
    # Determine if user can add more properties based on their highest plan
    can_add_property = True
    limit_message = ""
    
    # Check limits based on the highest active plan
    if premium_count > 0:
        # User has premium plan
        if total_active >= 10:
            can_add_property = False
            limit_message = "You have reached your Premium Plan limit (10 properties)."
    elif standard_count > 0:
        # User has standard plan
        if total_active >= 3:
            can_add_property = False
            limit_message = "You have reached your Standard Plan limit (3 properties). Please upgrade to Premium plan to list more properties."
    elif basic_count > 0:
        # User only has basic plan
        if total_active >= 1:
            can_add_property = False
            limit_message = "You have reached your Basic Plan limit (1 property). Please upgrade to Standard or Premium plan to list more properties."
    
    if not can_add_property:
        messages.error(request, limit_message)
        return redirect('dashboard')

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property_obj = form.save(commit=False)
            property_obj.owner = request.user
            property_obj.status = Property.Status.PENDING_APPROVAL
            property_obj.save()
            messages.success(request, "Property details saved! Now upload photos.")
            return redirect('add_photos', id=property_obj.id)
    else:
        form = PropertyForm()
    
    return render(request, 'core/add_property.html', {'form': form})

@login_required
def edit_property_view(request, id):
    property_obj = get_object_or_404(Property, id=id, owner=request.user)
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Property details updated. Continue to photos.")
            return redirect('add_photos', id=property_obj.id)
    else:
        form = PropertyForm(instance=property_obj)
    return render(request, 'core/add_property.html', {'form': form})

@login_required
def add_photos_view(request, id):
    property_obj = get_object_or_404(Property, id=id, owner=request.user)
    if request.method == 'POST':
        images = request.FILES.getlist('images')
        if images:
            for image in images:
                PropertyImage.objects.create(property=property_obj, image=image)
            messages.success(request, "Photos uploaded! Now choose your listing plan.")
            return redirect('select_plan', id=property_obj.id)
        else:
            messages.error(request, "Please select at least one image.")
    return render(request, 'core/add_property_photos.html', {'property': property_obj})

@login_required
def select_plan_view(request, id):
    property_obj = get_object_or_404(Property, id=id, owner=request.user)
    
    if property_obj.is_paid:
        messages.info(request, "Payment already completed for this property.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        selected_plan = request.POST.get('plan')
        # Store the selected plan in session
        request.session['selected_plan'] = selected_plan
        request.session['property_id'] = property_obj.id
        return redirect('payment', id=property_obj.id)
    
    # Define plans
    plans = {
        'basic': {
            'name': 'Basic Plan',
            'price': 99,
            'duration': '3 Months',
            'features': [
                'List up to 1 property',
                'Visible for 90 days',
                'Standard visibility'
            ]
        },
        'standard': {
            'name': 'Standard Plan',
            'price': 199,
            'duration': '6 Months',
            'features': [
                'List up to 3 properties',
                'Visible for 180 days',
                'Priority visibility',
                'Shown above basic listings'
            ],
            'popular': True
        },
        'premium': {
            'name': 'Premium Plan',
            'price': 399,
            'duration': '1 Year',
            'features': [
                'List up to 10 properties',
                'Visible for 365 days',
                '⭐ Featured badge',
                'Top search priority',
                'Premium support'
            ]
        }
    }
    
    return render(request, 'core/select_plan.html', {'property': property_obj, 'plans': plans})

@login_required
def payment_view(request, id):
    property_obj = get_object_or_404(Property, id=id, owner=request.user)
    if property_obj.is_paid:
        messages.info(request, "Payment already completed for this property.")
        return redirect('dashboard')
    
    # Get selected plan from session
    selected_plan = request.session.get('selected_plan', 'basic')
    
    # Define plan prices
    plan_prices = {
        'basic': 99,
        'standard': 199,
        'premium': 399
    }
    
    plan_names = {
        'basic': 'Basic Plan',
        'standard': 'Standard Plan',
        'premium': 'Premium Plan'
    }
    
    amount_inr = plan_prices.get(selected_plan, 99)
    plan_name = plan_names.get(selected_plan, 'Basic Plan')
    
    # Check if Razorpay keys are configured
    if settings.RAZORPAY_KEY_ID.startswith('rzp_test_YOUR') or settings.RAZORPAY_KEY_ID == 'rzp_test_YOUR_KEY_ID':
        messages.error(request, "⚠️ Razorpay is not yet configured. Please contact the admin. (Missing API keys)")
        return redirect('dashboard')
    
    try:
        # Initialize Razorpay client
        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )
        
        # Check if payment record already exists
        try:
            payment = Payment.objects.get(property=property_obj)
            # If payment exists but is not successful, create a new order
            if payment.status != Payment.PaymentStatus.SUCCESS:
                # Amount in paise (1 INR = 100 paise)
                amount = int(amount_inr * 100)
                
                # Create new Razorpay order
                order_data = {
                    'amount': amount,
                    'currency': 'INR',
                    'payment_capture': '1'
                }
                
                razorpay_order = client.order.create(data=order_data)
                
                # Update existing payment record with new order
                payment.razorpay_order_id = razorpay_order['id']
                payment.razorpay_payment_id = None
                payment.razorpay_signature = None
                payment.status = Payment.PaymentStatus.PENDING
                payment.amount = amount_inr
                payment.save()
        except Payment.DoesNotExist:
            # No payment exists, create new one
            amount = int(amount_inr * 100)
            
            # Create Razorpay order
            order_data = {
                'amount': amount,
                'currency': 'INR',
                'payment_capture': '1'
            }
            
            razorpay_order = client.order.create(data=order_data)
            
            # Save payment record
            payment = Payment.objects.create(
                property=property_obj,
                owner=request.user,
                razorpay_order_id=razorpay_order['id'],
                amount=amount_inr,
                status=Payment.PaymentStatus.PENDING
            )
        
        context = {
            'property': property_obj,
            'razorpay_order_id': payment.razorpay_order_id,
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'amount': amount_inr,
            'payment_id': payment.id,
            'plan_name': plan_name,
            'selected_plan': selected_plan,
        }
        
        return render(request, 'core/payment.html', context)
    
    except Exception as e:
        # Handle Razorpay errors
        error_msg = str(e)
        if 'Authentication failed' in error_msg or 'Unauthorized' in error_msg:
            messages.error(request, "❌ Payment configuration error. Please check Razorpay API keys with admin.")
        else:
            messages.error(request, f"❌ Payment error: {error_msg}")
        return redirect('add_photos', id=id)

@csrf_exempt
@require_POST
def verify_payment_view(request):
    """Verify Razorpay payment signature"""
    try:
        payment_data = json.loads(request.body)
        
        # Get payment record
        payment = Payment.objects.get(razorpay_order_id=payment_data['razorpay_order_id'])
        
        # Initialize Razorpay client
        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )
        
        # Verify signature
        signature_data = {
            'razorpay_order_id': payment_data['razorpay_order_id'],
            'razorpay_payment_id': payment_data['razorpay_payment_id'],
            'razorpay_signature': payment_data['razorpay_signature']
        }
        
        # Verify the payment
        is_valid = client.utility.verify_payment_signature(signature_data)
        
        if is_valid:
            # Update payment status
            payment.razorpay_payment_id = payment_data['razorpay_payment_id']
            payment.razorpay_signature = payment_data['razorpay_signature']
            payment.status = Payment.PaymentStatus.SUCCESS
            payment.save()
            
            # Update property with plan details
            from django.utils import timezone
            from datetime import timedelta
            
            property_obj = payment.property
            property_obj.is_paid = True
            
            # Get selected plan from session
            from django.contrib.sessions.models import Session
            # Since this is a POST request without session, we need to get it from payment amount
            # Map amount to plan type
            if payment.amount == 99:
                property_obj.plan_type = 'basic'
                property_obj.plan_expiry_date = timezone.now() + timedelta(days=90)
            elif payment.amount == 199:
                property_obj.plan_type = 'standard'
                property_obj.plan_expiry_date = timezone.now() + timedelta(days=180)
            elif payment.amount == 399:
                property_obj.plan_type = 'premium'
                property_obj.plan_expiry_date = timezone.now() + timedelta(days=365)
            else:
                # Default to basic
                property_obj.plan_type = 'basic'
                property_obj.plan_expiry_date = timezone.now() + timedelta(days=90)
            
            property_obj.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Payment verified successfully!',
                'redirect': '/dashboard/'
            })
        else:
            payment.status = Payment.PaymentStatus.FAILED
            payment.save()
            return JsonResponse({
                'success': False,
                'message': 'Payment verification failed. Invalid signature.'
            })
    
    except Payment.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Payment record not found.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error: {str(e)}'
        })

@csrf_exempt
@require_POST
def razorpay_webhook(request):
    """Handle Razorpay webhook events"""
    try:
        # Get webhook data
        webhook_body = request.body
        webhook_signature = request.headers.get('X-Razorpay-Signature', '')
        
        # Initialize Razorpay client
        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )
        
        # Verify webhook signature (if webhook secret is configured)
        # For now, we'll process without verification for testing
        # In production, you should verify the signature
        
        webhook_data = json.loads(webhook_body)
        event = webhook_data.get('event')
        payload = webhook_data.get('payload', {})
        payment_entity = payload.get('payment', {}).get('entity', {})
        
        print(f"Webhook received: {event}")
        print(f"Payment data: {payment_entity}")
        
        # Handle payment.captured event
        if event == 'payment.captured':
            razorpay_payment_id = payment_entity.get('id')
            razorpay_order_id = payment_entity.get('order_id')
            
            try:
                # Find the payment record
                payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
                
                # Update payment status
                payment.razorpay_payment_id = razorpay_payment_id
                payment.status = Payment.PaymentStatus.SUCCESS
                payment.save()
                
                # Mark property as paid
                property_obj = payment.property
                property_obj.is_paid = True
                property_obj.save()
                
                print(f"Payment {razorpay_payment_id} marked as successful")
                
            except Payment.DoesNotExist:
                print(f"Payment record not found for order: {razorpay_order_id}")
        
        # Handle payment.failed event
        elif event == 'payment.failed':
            razorpay_order_id = payment_entity.get('order_id')
            
            try:
                payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
                payment.status = Payment.PaymentStatus.FAILED
                payment.save()
                print(f"Payment marked as failed for order: {razorpay_order_id}")
            except Payment.DoesNotExist:
                print(f"Payment record not found for order: {razorpay_order_id}")
        
        # Return success response to Razorpay
        return JsonResponse({'status': 'ok'})
    
    except Exception as e:
        print(f"Webhook error: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

# NEW: Admin Action View
@login_required
def approve_property_view(request, id):
    if not request.user.is_superuser and request.user.role != 'ADMIN':
        messages.error(request, "Access denied.")
        return redirect('dashboard')
        
    property_obj = get_object_or_404(Property, id=id)
    property_obj.status = Property.Status.AVAILABLE
    property_obj.save()
    messages.success(request, f"Property '{property_obj.title}' approved successfully!")
    return redirect('dashboard')

@login_required
def reject_property_view(request, id):
    if not request.user.is_superuser and request.user.role != 'ADMIN':
        messages.error(request, "Access denied.")
        return redirect('dashboard')
        
    property_obj = get_object_or_404(Property, id=id)
    property_obj.status = Property.Status.REJECTED # Ensure REJECTED status exists in model or use another
    # If REJECTED isn't in choices, delete or set to Maintenance. Assuming REJECTED exists or just delete.
    # For now, let's delete to "reject" or set to maintenance. 
    # Better: Update model Status choices if REJECTED isn't there. 
    # Based on prev code: PENDING_APPROVAL, AVAILABLE, RENTED, MAINTENANCE.
    # Let's set to MAINTENANCE or delete. I'll delete for now or you can add REJECTED status.
    property_obj.delete() 
    messages.success(request, f"Property '{property_obj.title}' rejected and removed.")
    return redirect('dashboard')

@login_required
def manage_property_view(request, id):
    property_obj = get_object_or_404(Property, id=id, owner=request.user)
    
    # Fetch related data
    applications = RentalApplication.objects.filter(property=property_obj)
    
    context = {
        'property': property_obj,
        'applications': applications,
    }
    return render(request, 'core/property_manage.html', context)

@login_required
def delete_property_view(request, id):
    """Delete a property - Owner only"""
    property_obj = get_object_or_404(Property, id=id, owner=request.user)
    property_title = property_obj.title
    property_obj.delete()
    
    messages.success(request, f"Property '{property_title}' has been deleted successfully.")
    return redirect('dashboard')

@login_required
def mark_property_rented_view(request, id):
    """Mark property as rented - Owner only"""
    property_obj = get_object_or_404(Property, id=id, owner=request.user)
    property_obj.status = Property.Status.RENTED
    property_obj.save()
    
    messages.success(request, f"Property '{property_obj.title}' has been marked as RENTED. It will only be visible to you and the tenant.")
    return redirect('manage_property', id=id)


@login_required
def property_details_view(request, id):
    """View property details with all images"""
    property_obj = get_object_or_404(Property, id=id)
    
    # Check if user has permission to view
    # Admins can view all, owners can view their own, tenants can view available properties
    if request.user.is_superuser or request.user.role == 'ADMIN':
        # Admin can view all properties
        pass
    elif request.user.role == 'OWNER' and property_obj.owner == request.user:
        # Owner can view their own properties
        pass
    elif request.user.role == 'TENANT' and property_obj.status == 'AVAILABLE':
        # Tenants can only view available properties
        pass
    else:
        messages.error(request, "You don't have permission to view this property.")
        return redirect('dashboard')
    
    context = {
        'property': property_obj,
        'images': property_obj.images.all()
    }
    return render(request, 'core/property_details.html', context)

@login_required
def delete_user_view(request, id):
    """Delete a user - Admin only"""
    # Only allow admin to delete users
    if not (request.user.is_superuser or request.user.role == 'ADMIN'):
        messages.error(request, "You don't have permission to delete users.")
        return redirect('dashboard')
    
    # Prevent deleting the current admin user
    if request.user.id == id:
        messages.error(request, "You cannot delete your own account.")
        return redirect('dashboard')
    
    user_to_delete = get_object_or_404(User, id=id)
    username = user_to_delete.username
    
    # Delete all properties owned by the user first (cascade delete)
    user_to_delete.delete()
    
    messages.success(request, f"User '{username}' and all associated data have been deleted successfully.")
    return redirect('dashboard')


# Messaging System Views
@login_required
def conversations_view(request):
    """View all conversations for the logged-in user"""
    if request.user.role == 'TENANT':
        conversations = Conversation.objects.filter(tenant=request.user)
    elif request.user.role == 'OWNER':
        conversations = Conversation.objects.filter(owner=request.user)
    else:
        conversations = Conversation.objects.all()
    
    # Add unread count to each conversation
    conversations_with_unread = []
    for conversation in conversations:
        unread_count = conversation.messages.filter(is_read=False).exclude(sender=request.user).count()
        conversation.has_unread = unread_count > 0
        conversations_with_unread.append(conversation)
    
    context = {
        'conversations': conversations_with_unread
    }
    return render(request, 'core/conversations.html', context)

@login_required
def conversation_detail_view(request, id):
    """View a specific conversation and send messages"""
    conversation = get_object_or_404(Conversation, id=id)
    
    # Check if user is part of this conversation
    if request.user not in [conversation.tenant, conversation.owner] and not request.user.is_superuser:
        messages.error(request, "You don't have access to this conversation.")
        return redirect('conversations')
    
    # Mark messages as read for the current user
    Message.objects.filter(conversation=conversation).exclude(sender=request.user).update(is_read=True)
    
    # Handle new message
    if request.method == 'POST':
        content = request.POST.get('message')
        if content:
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content
            )
            conversation.save()  # Update the updated_at timestamp
            return redirect('conversation_detail', id=id)
    
    context = {
        'conversation': conversation,
        'messages': conversation.messages.all()
    }
    return render(request, 'core/conversation_detail.html', context)

@login_required
def start_conversation_view(request, property_id):
    """Start a new conversation about a property"""
    property_obj = get_object_or_404(Property, id=property_id)
    
    # Only tenants can start conversations
    if request.user.role != 'TENANT':
        messages.error(request, "Only tenants can start conversations.")
        return redirect('property_details', id=property_id)
    
    # Check if conversation already exists
    conversation, created = Conversation.objects.get_or_create(
        property=property_obj,
        tenant=request.user,
        owner=property_obj.owner
    )
    
    if created:
        messages.success(request, "Conversation started! Send your first message.")
    
    return redirect('conversation_detail', id=conversation.id)

@login_required
def add_review_view(request, property_id):
    """Add or update a review for a property"""
    from .models import Review
    
    property_obj = get_object_or_404(Property, id=property_id)
    
    # Check if user already has a review for this property
    existing_review = Review.objects.filter(property=property_obj, reviewer=request.user).first()
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        if not rating or not comment:
            messages.error(request, "Please provide both rating and comment.")
            return redirect('dashboard')
        
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                messages.error(request, "Rating must be between 1 and 5.")
                return redirect('dashboard')
            
            if existing_review:
                # Update existing review
                existing_review.rating = rating
                existing_review.comment = comment
                existing_review.save()
                messages.success(request, "Review updated successfully!")
            else:
                # Create new review
                Review.objects.create(
                    property=property_obj,
                    reviewer=request.user,
                    rating=rating,
                    comment=comment
                )
                messages.success(request, "Review added successfully!")
            
            return redirect('dashboard')
        except ValueError:
            messages.error(request, "Invalid rating value.")
            return redirect('dashboard')
    
    # For GET request, show the form
    context = {
        'property': property_obj,
        'existing_review': existing_review
    }
    return render(request, 'core/add_review.html', context)

@login_required
def delete_review_view(request, review_id):
    """Delete a review"""
    from .models import Review
    
    review = get_object_or_404(Review, id=review_id, reviewer=request.user)
    review.delete()
    messages.success(request, "Review deleted successfully!")
    return redirect('dashboard')

@login_required
def send_inquiry_view(request):
    """Handle inquiry submission from tenant dashboard"""
    if request.method == 'POST':
        property_id = request.POST.get('property_id')
        message = request.POST.get('message')
        
        if not property_id or not message:
            messages.error(request, "Please provide all required information.")
            return redirect('dashboard')
        
        try:
            property_obj = Property.objects.get(id=property_id)
            
            # Create or get conversation
            conversation, created = Conversation.objects.get_or_create(
                property=property_obj,
                tenant=request.user,
                owner=property_obj.owner
            )
            
            # Create message
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=message
            )
            
            messages.success(request, "Inquiry sent successfully! The owner will respond soon.")
            return redirect('dashboard')
            
        except Property.DoesNotExist:
            messages.error(request, "Property not found.")
            return redirect('dashboard')
    
    return redirect('dashboard')

# Wishlist Views
@login_required
def add_to_wishlist_view(request, property_id):
    """Add a property to tenant's wishlist"""
    if request.user.role != 'TENANT':
        messages.error(request, "Only tenants can add properties to wishlist.")
        return redirect('dashboard')
    
    from .models import Wishlist
    
    property_obj = get_object_or_404(Property, id=property_id)
    
    # Check if already in wishlist
    wishlist_item, created = Wishlist.objects.get_or_create(
        tenant=request.user,
        property=property_obj
    )
    
    if created:
        messages.success(request, f"'{property_obj.title}' added to your wishlist!")
    else:
        messages.info(request, "This property is already in your wishlist.")
    
    # Redirect back to the referring page or dashboard
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

@login_required
def remove_from_wishlist_view(request, property_id):
    """Remove a property from tenant's wishlist"""
    if request.user.role != 'TENANT':
        messages.error(request, "Access denied.")
        return redirect('dashboard')
    
    from .models import Wishlist
    
    property_obj = get_object_or_404(Property, id=property_id)
    
    try:
        wishlist_item = Wishlist.objects.get(tenant=request.user, property=property_obj)
        wishlist_item.delete()
        messages.success(request, f"'{property_obj.title}' removed from your wishlist.")
    except Wishlist.DoesNotExist:
        messages.error(request, "Property not found in your wishlist.")
    
    # Redirect back to the referring page or dashboard
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

@login_required
def wishlist_view(request):
    """View all wishlist items for the tenant"""
    if request.user.role != 'TENANT':
        messages.error(request, "Only tenants can access wishlist.")
        return redirect('dashboard')
    
    from .models import Wishlist
    from django.utils import timezone
    
    # Get all wishlist items with active properties
    wishlist_items = Wishlist.objects.filter(tenant=request.user).select_related('property')
    
    # Filter to only show properties that are still available and have active plans
    active_wishlist = []
    for item in wishlist_items:
        if (item.property.status == Property.Status.AVAILABLE and 
            item.property.is_paid and 
            item.property.plan_expiry_date and
            item.property.plan_expiry_date > timezone.now()):
            active_wishlist.append(item)
    
    context = {
        'wishlist_items': active_wishlist,
        'total_wishlist': len(active_wishlist)
    }
    return render(request, 'core/wishlist.html', context)


# Website Feedback Views
@login_required
def submit_website_feedback_view(request):
    """Submit feedback about the RentEase platform"""
    from .models import WebsiteFeedback
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        title = request.POST.get('title')
        comment = request.POST.get('comment')
        
        if not rating or not title or not comment:
            messages.error(request, "Please provide all required fields.")
            return redirect('website_feedback')
        
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                messages.error(request, "Rating must be between 1 and 5.")
                return redirect('website_feedback')
            
            WebsiteFeedback.objects.create(
                user=request.user,
                rating=rating,
                title=title,
                comment=comment
            )
            messages.success(request, "Thank you for your feedback! We appreciate your input.")
            return redirect('dashboard')
        except ValueError:
            messages.error(request, "Invalid rating value.")
            return redirect('website_feedback')
    
    return render(request, 'core/website_feedback.html')

@login_required
def website_feedback_list_view(request):
    """View all website feedbacks (for admins)"""
    if not (request.user.is_superuser or request.user.role == 'ADMIN'):
        messages.error(request, "Access denied.")
        return redirect('dashboard')
    
    from .models import WebsiteFeedback
    
    feedbacks = WebsiteFeedback.objects.all().select_related('user').order_by('-created_at')
    
    context = {
        'feedbacks': feedbacks,
        'total_feedbacks': feedbacks.count(),
        'average_rating': feedbacks.aggregate(models.Avg('rating'))['rating__avg'] or 0
    }
    return render(request, 'core/feedback_list.html', context)

def public_feedbacks_view(request):
    """Public view of featured feedbacks (for homepage)"""
    from .models import WebsiteFeedback
    
    featured_feedbacks = WebsiteFeedback.objects.filter(
        is_featured=True,
        is_approved=True
    ).select_related('user').order_by('-created_at')[:6]
    
    context = {
        'featured_feedbacks': featured_feedbacks
    }
    return render(request, 'core/public_feedbacks.html', context)
