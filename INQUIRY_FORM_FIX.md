# Inquiry Form Fix - Tenant Dashboard

## Problem
When tenants tried to send inquiries from the tenant dashboard, they encountered an error. The form submission was failing.

## Root Causes Identified

### 1. Missing Form Action URL
The inquiry modal form had an empty action attribute:
```html
<form id="inquiryForm" method="POST" action="">
```

This caused the form to submit to the current page (dashboard) instead of the `send_inquiry` endpoint.

### 2. Missing Import in views.py
The `send_inquiry_view` function used `reverse()` to build the conversation URL for email notifications, but the `reverse` function was not imported:
```python
conversation_url = request.build_absolute_uri(reverse('conversation_detail', args=[conversation.id]))
```

This would cause a `NameError: name 'reverse' is not defined` when the view tried to execute.

## Solutions Applied

### Fix 1: Added Form Action URL
Updated the inquiry form to point to the correct endpoint:
```html
<form id="inquiryForm" method="POST" action="{% url 'send_inquiry' %}">
```

### Fix 2: Added Missing Import
Added the `reverse` import to views.py:
```python
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse  # Added this line
from django.contrib.auth import authenticate, login, logout, get_user_model
```

## How It Works Now

### Inquiry Flow
1. Tenant clicks "SEND INQUIRY" button on a property card
2. Modal opens with property details pre-filled
3. Tenant can use quick suggestions or type custom message
4. Form submits to `/send-inquiry/` endpoint
5. `send_inquiry_view` processes the request:
   - Validates property_id and message
   - Creates or retrieves conversation between tenant and owner
   - Creates a new message in the conversation
   - Sends email notification to property owner
   - Redirects tenant to dashboard with success message

### Features
- Quick suggestion buttons for common inquiries
- Character counter (500 max)
- Email notification to property owner
- Conversation thread created automatically
- Error handling for missing data

## Files Modified
1. `core/views.py` - Added `reverse` import
2. `core/templates/core/tenant_dashboard.html` - Fixed form action URL

## Testing Checklist
- [x] Form action URL points to correct endpoint
- [x] Missing import added
- [x] No syntax errors or diagnostics
- [ ] Test sending inquiry from tenant dashboard
- [ ] Verify conversation is created
- [ ] Verify message is saved
- [ ] Verify email notification is sent to owner
- [ ] Verify success message displays
- [ ] Verify tenant is redirected to dashboard

## Related URLs
- Inquiry submission: `/send-inquiry/` (POST)
- Conversations list: `/conversations/`
- Conversation detail: `/conversation/<id>/`
