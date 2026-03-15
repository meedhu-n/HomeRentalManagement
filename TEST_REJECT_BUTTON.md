# Test Reject Button - Step by Step

## The reject button IS properly implemented. Follow these steps to test:

### Step 1: Login as Admin
1. Go to: `http://localhost:8000/login/`
2. Login with admin credentials
3. You should see the admin dashboard

### Step 2: Find Pending Property
1. Look for "PENDING APPROVALS" section
2. You should see at least one property waiting for approval
3. Each property has three buttons: VIEW DETAILS, APPROVE, REJECT

### Step 3: Click REJECT Button
1. Click the red "REJECT" button
2. A modal (popup) should appear with:
   - Title: "Reject Property"
   - Property name in red
   - Textarea for rejection reason
   - Cancel and "Reject Property" buttons

### Step 4: Enter Rejection Reason
1. Click in the textarea
2. Type a reason (e.g., "Property images are unclear")
3. The textarea is REQUIRED - you must enter something

### Step 5: Submit Rejection
1. Click the red "Reject Property" button at the bottom
2. The modal should close
3. Page should refresh
4. You should see a success message: "Property has been rejected"
5. The property should disappear from pending list

### Step 6: Verify Rejection
1. Scroll down to "ALL PROPERTIES" section
2. Find the rejected property
3. It should show status as "REJECTED"

### Step 7: Check Owner Dashboard
1. Logout from admin
2. Login as the property owner
3. Go to dashboard
4. Scroll to "Rejected Properties" section
5. You should see the rejected property with the rejection reason displayed

## If Modal Doesn't Open

### Check 1: Browser Console
1. Press F12 to open developer tools
2. Click "Console" tab
3. Click REJECT button
4. Look for error messages (red text)
5. You should see: "Reject button clicked for property X"

### Check 2: Bootstrap Loaded
1. In console, type: `typeof bootstrap`
2. Press Enter
3. Should show: "object" (not "undefined")

### Check 3: Modal Exists
1. In console, type: `document.getElementById('rejectModal1')`
2. Press Enter
3. Should show: `<div class="modal fade"...>` (not null)

## If Form Doesn't Submit

### Check 1: Required Field
- Make sure you entered text in the rejection reason textarea
- The field is required and won't submit if empty

### Check 2: Network Request
1. Open F12 → Network tab
2. Enter rejection reason
3. Click "Reject Property"
4. Look for a POST request to `/admin-reject/X/`
5. Status should be 302 (redirect)

### Check 3: CSRF Token
1. Right-click on page → View Page Source
2. Search for: `csrfmiddlewaretoken`
3. Should find it inside the form

## Quick Test Commands

### Test 1: Check if property exists
```bash
python manage.py shell -c "from core.models import Property; print('Pending:', Property.objects.filter(status='PENDING', is_paid=True).count())"
```

### Test 2: Check if admin exists
```bash
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); print('Admins:', User.objects.filter(is_superuser=True).count())"
```

### Test 3: Check URL routing
```bash
python manage.py shell -c "from django.urls import reverse; print('Reject URL:', reverse('reject_property', args=[1]))"
```

## Manual Rejection (If Button Still Doesn't Work)

### Option 1: Django Admin
1. Go to: `http://localhost:8000/admin/`
2. Login with superuser credentials
3. Click "Properties"
4. Find the property
5. Change status to "REJECTED"
6. Add rejection reason in the field
7. Click "Save"

### Option 2: Django Shell
```python
python manage.py shell

from core.models import Property
from core.email_utils import send_property_rejection_notification

# Get the property
prop = Property.objects.get(id=1)  # Change ID as needed

# Reject it
prop.status = 'REJECTED'
prop.rejection_reason = 'Your rejection reason here'
prop.save()

# Send email
send_property_rejection_notification(
    property_owner=prop.owner,
    property_title=prop.title,
    rejection_reason=prop.rejection_reason,
    dashboard_url='http://localhost:8000/dashboard/'
)

print("Property rejected successfully!")
```

## What I've Added for Debugging

I've added console.log statements to help identify where the issue is:

1. **Button click**: Shows when REJECT button is clicked
2. **Textarea input**: Shows what you're typing
3. **Form submit**: Shows when form is being submitted
4. **Submit button**: Shows when submit button is clicked

**Check your browser console (F12) to see these messages!**

## Expected Console Output

When everything works correctly, you should see:
```
Reject button clicked for property 1
Rejection reason: [your text as you type]
Submit button clicked
Form submitting for property 1
```

Then the page should redirect and show success message.

## Common Mistakes

1. ❌ Not entering rejection reason (field is required)
2. ❌ Clicking outside modal (closes it without submitting)
3. ❌ Clicking Cancel instead of Reject Property
4. ❌ Not logged in as admin
5. ❌ Browser cache showing old version (try Ctrl+F5)

## Force Refresh

If you've made changes and button still doesn't work:
1. Press Ctrl+Shift+Delete
2. Clear cache and cookies
3. Close browser completely
4. Reopen and try again

OR

1. Press Ctrl+F5 (hard refresh)
2. Try again

## Still Not Working?

Please check browser console (F12) and tell me:
1. What messages appear when you click REJECT?
2. Are there any red error messages?
3. Does the modal open at all?
4. Can you type in the textarea?
5. What happens when you click "Reject Property"?

This will help me identify the exact issue!
