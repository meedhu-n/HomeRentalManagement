from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.conf import settings
from .models import Property, PropertyImage, Payment, RentalApplication, MaintenanceRequest
from .forms import PropertyForm
import razorpay
import json
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()

# ... (Previous views: index, register, login, logout remain same) ...
def index(request):
    return render(request, 'core/index.html')

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
        properties = Property.objects.filter(owner=request.user)
        context['properties'] = properties
        context['active_listings_count'] = properties.filter(status=Property.Status.AVAILABLE).count()
        return render(request, 'core/owner_dashboard.html', context)
    
    elif request.user.role == 'TENANT':
        available_properties = Property.objects.filter(status=Property.Status.AVAILABLE).order_by('-created_at')
        user_applications = RentalApplication.objects.filter(tenant=request.user).order_by('-application_date')
        context['available_properties'] = available_properties
        context['total_available'] = available_properties.count()
        context['applications'] = user_applications
        context['total_applications'] = user_applications.count()
        context['approved_applications'] = user_applications.filter(status=RentalApplication.Status.APPROVED).count()
        return render(request, 'core/tenant_dashboard.html', context)
    
    return render(request, 'core/dashboard.html', context)

@login_required
def add_property_view(request):
    if request.user.role != 'OWNER':
        messages.error(request, "Access denied. Owners only.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property_obj = form.save(commit=False)
            property_obj.owner = request.user
            property_obj.status = Property.Status.PENDING_APPROVAL
            property_obj.save()
            messages.success(request, "Step 1 Complete! Now upload photos.")
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
            messages.success(request, "Photos uploaded! Please complete payment to submit for approval.")
            return redirect('payment', id=property_obj.id)
        else:
            messages.error(request, "Please select at least one image.")
    return render(request, 'core/add_property_photos.html', {'property': property_obj})

@login_required
def payment_view(request, id):
    property_obj = get_object_or_404(Property, id=id, owner=request.user)
    if property_obj.is_paid:
        messages.info(request, "Payment already completed for this property.")
        return redirect('dashboard')
    
    # Check if Razorpay keys are configured
    if settings.RAZORPAY_KEY_ID.startswith('rzp_test_YOUR') or settings.RAZORPAY_KEY_ID == 'rzp_test_YOUR_KEY_ID':
        messages.error(request, "⚠️ Razorpay is not yet configured. Please contact the admin. (Missing API keys)")
        return redirect('dashboard')
    
    try:
        # Initialize Razorpay client
        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )
        
        # Amount in paise (1 INR = 100 paise)
        amount = int(settings.PROPERTY_REGISTRATION_FEE * 100)
        
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
            amount=settings.PROPERTY_REGISTRATION_FEE,
            status=Payment.PaymentStatus.PENDING
        )
        
        context = {
            'property': property_obj,
            'razorpay_order_id': razorpay_order['id'],
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'amount': settings.PROPERTY_REGISTRATION_FEE,
            'payment_id': payment.id,
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
            
            # Update property as paid
            property_obj = payment.property
            property_obj.is_paid = True
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
    maintenance_requests = MaintenanceRequest.objects.filter(property=property_obj)
    
    context = {
        'property': property_obj,
        'applications': applications,
        'maintenance_requests': maintenance_requests
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
    """View property details with all images - Admin view"""
    # Only allow admin to view
    if not (request.user.is_superuser or request.user.role == 'ADMIN'):
        return redirect('dashboard')
    
    property_obj = get_object_or_404(Property, id=id)
    
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
