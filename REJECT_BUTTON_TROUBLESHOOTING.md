# Reject Button Troubleshooting Guide

## Current Implementation

The reject button is properly implemented with:
1. ✅ Modal trigger button
2. ✅ Bootstrap modal with form
3. ✅ POST form with CSRF token
4. ✅ Required textarea for rejection reason
5. ✅ Backend view to handle rejection
6. ✅ Email notification to owner
7. ✅ URL routing configured

## How to Test

### Step 1: Open Browser Console
1. Open admin dashboard
2. Press F12 (or Ctrl+Shift+I)
3. Go to "Console" tab

### Step 2: Click Reject Button
When you click the REJECT button, you should see:
```
Reject button clicked for property X
```

### Step 3: Enter Rejection Reason
Type in the textarea, you should see:
```
Rejection reason: [your text]
```

### Step 4: Click Submit
When you click "Reject Property" button, you should see:
```
Submit button clicked
Form submitting for property X
```

## Common Issues & Solutions

### Issue 1: Modal Doesn't Open
**Symptoms**: Clicking REJECT button does nothing

**Possible Causes**:
1. Bootstrap JS not loaded
2. JavaScript error blocking execution
3. Modal ID mismatch

**Solutions**:
```html
<!-- Check if Bootstrap is loaded -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

<!-- Verify modal ID matches button target -->
<button data-bs-target="#rejectModal123">REJECT</button>
<div id="rejectModal123">...</div>
```

### Issue 2: Form Doesn't Submit
**Symptoms**: Modal opens but clicking submit does nothing

**Possible Causes**:
1. Form action URL incorrect
2. CSRF token missing
3. JavaScript preventing submission
4. Required field validation failing

**Solutions**:
```html
<!-- Ensure form has correct action -->
<form method="POST" action="{% url 'reject_property' property.id %}">
    {% csrf_token %}
    <textarea name="rejection_reason" required></textarea>
    <button type="submit">Submit</button>
</form>
```

### Issue 3: Backend Error
**Symptoms**: Form submits but shows error or redirects without action

**Possible Causes**:
1. View not receiving POST data
2. Permission check failing
3. Database error

**Check Django Logs**:
```bash
# Run server and watch for errors
python manage.py runserver

# Check for error messages when submitting
```

## Debugging Steps

### 1. Check Browser Console
Look for JavaScript errors:
- Red error messages
- Failed network requests
- Console.log messages

### 2. Check Network Tab
1. Open F12 → Network tab
2. Click Reject button
3. Enter reason and submit
4. Look for POST request to `/admin-reject/X/`
5. Check response status (should be 302 redirect)

### 3. Check Django Server Output
Watch terminal for:
```
POST /admin-reject/1/ HTTP/1.1" 302
```

### 4. Test Direct URL
Try accessing reject URL directly:
```
http://localhost:8000/admin-reject/1/
```
Should show "Method not allowed" (GET not supported)

## Manual Test

### Test the View Directly:
```python
# In Django shell
python manage.py shell

from core.models import Property
from django.contrib.auth import get_user_model

User = get_user_model()
admin = User.objects.filter(is_superuser=True).first()
property_obj = Property.objects.filter(status='PENDING').first()

print(f"Admin: {admin}")
print(f"Property: {property_obj}")
print(f"Property ID: {property_obj.id}")
```

### Test URL Resolution:
```python
from django.urls import reverse
print(reverse('reject_property', args=[1]))
# Should print: /admin-reject/1/
```

## Current Code Structure

### Button (admin_dashboard.html):
```html
<button type="button" 
        class="btn btn-danger btn-sm px-4" 
        data-bs-toggle="modal" 
        data-bs-target="#rejectModal{{ property.id }}"
        onclick="console.log('Reject button clicked for property {{ property.id }}')">
    REJECT
</button>
```

### Modal (admin_dashboard.html):
```html
<div class="modal fade" id="rejectModal{{ property.id }}" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
            <form method="POST" action="{% url 'reject_property' property.id %}">
                {% csrf_token %}
                <div class="modal-body">
                    <textarea name="rejection_reason" required></textarea>
                </div>
                <div class="modal-footer">
                    <button type="button" data-bs-dismiss="modal">Cancel</button>
                    <button type="submit">Reject Property</button>
                </div>
            </form>
        </div>
    </div>
</div>
```

### View (core/views.py):
```python
@login_required
def reject_property_view(request, id):
    if not request.user.is_superuser and request.user.role != 'ADMIN':
        messages.error(request, "Access denied.")
        return redirect('dashboard')
    
    property_obj = get_object_or_404(Property, id=id)
    
    if request.method == 'POST':
        rejection_reason = request.POST.get('rejection_reason', '').strip()
        
        if not rejection_reason:
            messages.error(request, "Please provide a reason for rejection.")
            return redirect('dashboard')
        
        property_title = property_obj.title
        property_owner = property_obj.owner
        
        property_obj.status = Property.Status.REJECTED
        property_obj.rejection_reason = rejection_reason
        property_obj.save()
        
        # Send email notification
        from .email_utils import send_property_rejection_notification
        dashboard_url = request.build_absolute_uri('/dashboard/')
        
        try:
            send_property_rejection_notification(
                property_owner=property_owner,
                property_title=property_title,
                rejection_reason=rejection_reason,
                dashboard_url=dashboard_url
            )
        except Exception as e:
            print(f"Failed to send rejection email: {e}")
        
        messages.success(request, f"Property '{property_title}' has been rejected.")
        return redirect('dashboard')
    
    messages.error(request, "Invalid request method.")
    return redirect('dashboard')
```

### URL (core/urls.py):
```python
path('admin-reject/<int:id>/', views.reject_property_view, name='reject_property'),
```

## What to Check Now

1. **Open admin dashboard in browser**
2. **Open browser console (F12)**
3. **Click REJECT button**
4. **Check console for messages**
5. **Enter rejection reason**
6. **Click "Reject Property"**
7. **Check console and network tab**
8. **Check Django terminal for POST request**

## Expected Behavior

1. Click REJECT → Modal opens
2. Enter reason → Text appears in textarea
3. Click submit → Form submits
4. Page redirects → Back to dashboard
5. Success message → "Property has been rejected"
6. Property status → Changed to REJECTED
7. Email sent → Owner receives notification

## If Still Not Working

### Quick Fix - Try Direct Link:
Add a direct link as backup:
```html
<a href="{% url 'reject_property' property.id %}" 
   onclick="return confirm('Are you sure? This requires a rejection reason.')">
    REJECT (Direct)
</a>
```

### Alternative - Use GET with Confirmation:
Change view to accept GET with confirmation page:
```python
def reject_property_view(request, id):
    property_obj = get_object_or_404(Property, id=id)
    
    if request.method == 'GET':
        # Show confirmation page with form
        return render(request, 'core/reject_confirm.html', {'property': property_obj})
    
    if request.method == 'POST':
        # Process rejection
        ...
```

## Status
🔧 **DEBUGGING MODE ACTIVE**

Console logging added to:
- Reject button click
- Textarea input
- Form submission
- Submit button click

Check browser console for these messages to identify where the process fails.
