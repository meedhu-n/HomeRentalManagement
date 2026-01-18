from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Property
from .forms import PropertyForm

User = get_user_model()

def index(request):
    """
    Renders the public landing page (Home).
    """
    return render(request, 'core/index.html')

def register_view(request):
    """
    Handles user registration for Tenants and Owners.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        role = request.POST.get('role')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Basic Validation
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'core/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'core/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'core/register.html')

        # Create User
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
    """
    Handles user login.
    """
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
    """
    Handles user logout.
    """
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('index')

@login_required
def dashboard_view(request):
    """
    Renders the dashboard based on user role.
    """
    context = {'user': request.user}
    
    if request.user.role == 'OWNER':
        # Fetch properties owned by this user
        properties = Property.objects.filter(owner=request.user)
        context['properties'] = properties
        context['active_listings_count'] = properties.count()
        return render(request, 'core/owner_dashboard.html', context)
    
    elif request.user.role == 'TENANT':
        # Add tenant specific context here if needed
        return render(request, 'core/tenant_dashboard.html', context)
    
    # Fallback or admin dashboard
    return render(request, 'core/dashboard.html', context)

@login_required
def add_property_view(request):
    """
    Allows owners to add a new property.
    """
    if request.user.role != 'OWNER':
        messages.error(request, "Access denied. Owners only.")
        return redirect('dashboard')

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property_obj = form.save(commit=False)
            property_obj.owner = request.user
            property_obj.save()
            messages.success(request, "Property listed successfully!")
            return redirect('dashboard')
    else:
        form = PropertyForm()
    
    return render(request, 'core/add_property.html', {'form': form})