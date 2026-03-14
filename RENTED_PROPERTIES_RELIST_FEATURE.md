# Rented Properties Re-listing Feature

## Overview

Added a comprehensive feature for property owners to view their rented properties and re-list them with new subscription payments when they become available again.

## Features Implemented

### 1. Rented Properties Section

**Location:** Owner Dashboard

**Display:**
- Separate section showing all properties marked as "RENTED"
- Count of rented properties in section header
- Visual distinction with blue border and slightly desaturated images
- Special "RENTED" badge with handshake icon

**Information Shown:**
- Property title and location
- Property stats (bedrooms, bathrooms, area, views)
- Last rental price
- "Re-List Property" button (green gradient)

### 2. Re-listing Workflow

**Step-by-Step Process:**

1. **Owner Views Rented Properties**
   - Navigate to Owner Dashboard
   - Scroll to "Rented Properties" section
   - See all properties currently rented out

2. **Click "Re-List Property"**
   - Green button with refresh icon
   - Redirects to plan selection page

3. **Select Subscription Plan**
   - Choose from Basic (₹99), Standard (₹199), or Premium (₹399)
   - Same plans as new property listing

4. **Complete Payment**
   - Razorpay payment gateway
   - Secure payment processing

5. **Property Status Update**
   - After successful payment:
     - Status changes from RENTED → PENDING_APPROVAL
     - New plan type assigned
     - New expiry date set
     - Property goes through admin approval again

6. **Admin Approval**
   - Admin reviews the re-listed property
   - Approves or rejects
   - Once approved, property becomes AVAILABLE again

### 3. Visual Design

**Rented Properties Cards:**
- Blue border (rgba(74, 144, 226, 0.3))
- Slightly desaturated images (20% grayscale)
- Blue "RENTED" badge with handshake icon
- Green "Re-List Property" button
- Same property stats as active listings

**Section Header:**
- Handshake icon in blue
- Count of rented properties
- Descriptive text explaining the feature

## Technical Implementation

### Backend Changes

**1. Updated `dashboard_view()` in core/views.py:**

```python
# Separate properties by status
rented_properties = properties.filter(status=Property.Status.RENTED).order_by('-updated_at')
active_properties = properties.exclude(status=Property.Status.RENTED)

# Add to context
context['properties'] = active_properties
context['rented_properties'] = rented_properties
context['rented_count'] = rented_properties.count()
```

**2. Created `relist_property_view()` in core/views.py:**

```python
@login_required
def relist_property_view(request, id):
    """Re-list a rented property - Owner only"""
    property_obj = get_object_or_404(Property, id=id, owner=request.user)
    
    # Check if property is actually rented
    if property_obj.status != Property.Status.RENTED:
        messages.error(request, "Only rented properties can be re-listed.")
        return redirect('dashboard')
    
    # Store property ID in session for payment flow
    request.session['relist_property_id'] = property_obj.id
    
    # Redirect to plan selection
    return redirect('select_plan', id=property_obj.id)
```

**3. Updated `verify_payment_view()` in core/views.py:**

```python
# If property was rented and being re-listed, set to pending approval
if property_obj.status == Property.Status.RENTED:
    property_obj.status = Property.Status.PENDING_APPROVAL

property_obj.save()
```

**4. Added URL pattern in core/urls.py:**

```python
path('relist-property/<int:id>/', views.relist_property_view, name='relist_property'),
```

### Frontend Changes

**Updated owner_dashboard.html:**

Added new section after active properties:
- Conditional display (only if rented_properties exist)
- Grid layout matching active properties
- Special styling for rented status
- Re-list button with green gradient

## User Flow Diagram

```
┌─────────────────────────┐
│  Owner Dashboard        │
│  - Active Properties    │
│  - Rented Properties ✓  │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Click "Re-List"        │
│  on Rented Property     │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Select Plan            │
│  - Basic (₹99)          │
│  - Standard (₹199)      │
│  - Premium (₹399)       │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Payment Gateway        │
│  (Razorpay)             │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Payment Success        │
│  Status: RENTED →       │
│  PENDING_APPROVAL       │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Admin Approval         │
│  Required               │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│  Property AVAILABLE     │
│  Listed Again!          │
└─────────────────────────┘
```

## Benefits

### For Property Owners

1. **Easy Re-listing** - No need to re-enter property details
2. **Maintain History** - Keep property ID and previous data
3. **Quick Process** - Just select plan and pay
4. **View Archive** - See all rented properties in one place
5. **Flexible Timing** - Re-list whenever tenant moves out

### For Platform

1. **Recurring Revenue** - Owners pay again to re-list
2. **Data Retention** - Property data preserved
3. **Quality Control** - Admin approval for re-listings
4. **User Engagement** - Owners return to platform

### For Tenants

1. **Updated Listings** - Fresh availability status
2. **Accurate Information** - Property details maintained
3. **Trust** - Admin-approved re-listings

## Property Status Flow

```
NEW PROPERTY
    ↓
PENDING_APPROVAL (after payment)
    ↓
AVAILABLE (after admin approval)
    ↓
RENTED (owner marks as rented)
    ↓
[Owner clicks Re-List]
    ↓
PENDING_APPROVAL (after new payment)
    ↓
AVAILABLE (after admin approval)
```

## Payment Plans

Same plans as new listings:

| Plan | Price | Duration | Properties | Features |
|------|-------|----------|------------|----------|
| Basic | ₹99 | 3 months | 1 | Standard visibility |
| Standard | ₹199 | 6 months | 3 | Priority visibility |
| Premium | ₹399 | 1 year | 10 | Featured badge, top priority |

## Security & Validation

**Checks Implemented:**

1. **Owner Verification** - Only property owner can re-list
2. **Status Validation** - Only RENTED properties can be re-listed
3. **Payment Required** - Must complete payment to re-list
4. **Admin Approval** - Re-listed properties need approval
5. **Session Management** - Property ID stored in session

## Database Changes

**No schema changes required!**

Uses existing fields:
- `status` - Changes from RENTED to PENDING_APPROVAL
- `plan_type` - Updated with new plan
- `plan_expiry_date` - Set to new expiry date
- `is_paid` - Set to True after payment

## Testing Checklist

- [x] Owner can view rented properties
- [x] Re-list button appears only for rented properties
- [x] Plan selection works for re-listing
- [x] Payment flow completes successfully
- [x] Property status updates correctly
- [x] Admin can approve re-listed properties
- [x] Property becomes available after approval
- [x] Non-owners cannot re-list others' properties

## Future Enhancements (Optional)

1. **Bulk Re-listing** - Re-list multiple properties at once
2. **Auto Re-list** - Schedule automatic re-listing
3. **Discount Codes** - Offer discounts for re-listings
4. **Notification System** - Email when property is rented/available
5. **Rental History** - Track how many times property was rented
6. **Tenant Feedback** - Collect feedback from previous tenants
7. **Quick Edit** - Update property details before re-listing
8. **Price Suggestions** - AI-powered price recommendations

## Files Modified

1. **core/views.py**
   - Updated `dashboard_view()` to separate rented properties
   - Added `relist_property_view()` function
   - Updated `verify_payment_view()` to handle re-listing

2. **core/urls.py**
   - Added `relist_property` URL pattern

3. **core/templates/core/owner_dashboard.html**
   - Added "Rented Properties" section
   - Added re-list button styling

## Access Control

**Who can re-list:** Property owners only
**Validation:** Property must be in RENTED status
**Payment:** Required for all re-listings
**Approval:** Admin approval required after payment

---

**Feature Status:** ✅ Complete and Working

**Added:** March 14, 2026

**Tested:** Yes

**Security:** Owner-only access enforced

**Payment:** Razorpay integration working

**Admin Approval:** Required for re-listings
