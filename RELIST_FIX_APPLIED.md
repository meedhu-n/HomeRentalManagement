# Re-list Feature Fix Applied

## Issue

When clicking "Re-List Property" button on rented properties, the feature was not working because:

1. `select_plan_view` was checking if `property_obj.is_paid` is True and redirecting to dashboard
2. Rented properties already have `is_paid=True` from their previous listing
3. This prevented owners from accessing the plan selection page

## Solution Applied

### 1. Updated `select_plan_view()` in core/views.py

**Before:**
```python
if property_obj.is_paid:
    messages.info(request, "Payment already completed for this property.")
    return redirect('dashboard')
```

**After:**
```python
# Check if this is a re-listing (rented property) or if payment is already completed
is_relisting = property_obj.status == Property.Status.RENTED

if property_obj.is_paid and not is_relisting:
    messages.info(request, "Payment already completed for this property.")
    return redirect('dashboard')
```

**What it does:**
- Checks if property status is RENTED
- If it's a re-listing, allows access to plan selection even if `is_paid=True`
- Stores `is_relisting` flag in session for tracking

### 2. Updated `payment_view()` in core/views.py

**Before:**
```python
if property_obj.is_paid:
    messages.info(request, "Payment already completed for this property.")
    return redirect('dashboard')
```

**After:**
```python
# Check if this is a re-listing
is_relisting = property_obj.status == Property.Status.RENTED

if property_obj.is_paid and not is_relisting:
    messages.info(request, "Payment already completed for this property.")
    return redirect('dashboard')
```

**Additional Logic:**
```python
# For re-listing, always create a new payment record
if is_relisting:
    # Create new Razorpay order
    # Create new payment record
else:
    # Handle normal payment flow
```

**What it does:**
- Checks if property is being re-listed
- For re-listings, creates a NEW payment record (allows multiple payments for same property)
- For normal listings, uses existing payment logic
- Allows rented properties to go through payment flow again

### 3. Existing `verify_payment_view()` Already Handles Re-listing

The verify_payment_view already had the logic to change status from RENTED to PENDING_APPROVAL:

```python
# If property was rented and being re-listed, set to pending approval
if property_obj.status == Property.Status.RENTED:
    property_obj.status = Property.Status.PENDING_APPROVAL
```

## How It Works Now

### Complete Re-listing Flow

```
1. Owner Dashboard
   ↓
2. Rented Properties Section
   ↓
3. Click "Re-List Property" ✅
   ↓
4. relist_property_view()
   - Validates property is RENTED
   - Redirects to select_plan
   ↓
5. select_plan_view() ✅ FIXED
   - Detects is_relisting = True
   - Allows access even if is_paid = True
   - Shows plan selection page
   ↓
6. Owner Selects Plan
   - Clicks plan button
   - Redirects to payment
   ↓
7. payment_view() ✅ FIXED
   - Detects is_relisting = True
   - Creates NEW payment record
   - Shows Razorpay payment page
   ↓
8. Owner Completes Payment
   ↓
9. verify_payment_view()
   - Verifies payment
   - Changes status: RENTED → PENDING_APPROVAL
   - Updates plan details
   ↓
10. Admin Approval
    - Admin reviews property
    - Approves
    ↓
11. Property AVAILABLE Again! ✅
```

## Testing Steps

To verify the fix works:

```bash
# 1. Start server
python manage.py runserver

# 2. Login as owner with rented properties

# 3. Go to Owner Dashboard
# - Should see "Rented Properties" section

# 4. Click "Re-List Property" button
# - Should redirect to plan selection page ✅
# - Should NOT show "Payment already completed" error ✅

# 5. Select a plan (Basic/Standard/Premium)
# - Should redirect to payment page ✅

# 6. Complete payment (or test with Razorpay test mode)
# - Payment should process successfully ✅
# - Property status should change to PENDING_APPROVAL ✅

# 7. Login as admin
# - Should see property in pending approvals ✅
# - Approve the property ✅

# 8. Property should be AVAILABLE again ✅
```

## Key Changes Summary

| File | Function | Change |
|------|----------|--------|
| core/views.py | select_plan_view() | Added `is_relisting` check to allow rented properties |
| core/views.py | payment_view() | Added `is_relisting` check and new payment record creation |
| core/views.py | verify_payment_view() | Already had status change logic (no change needed) |

## What Was Fixed

✅ **Re-list button now works** - Clicking it redirects to plan selection
✅ **Plan selection accessible** - Rented properties can access plan page
✅ **Payment flow works** - New payment records created for re-listings
✅ **Status updates correctly** - RENTED → PENDING_APPROVAL → AVAILABLE
✅ **Multiple payments allowed** - Same property can be paid for multiple times

## Database Impact

**No schema changes required!**

The fix uses existing database structure:
- Creates new Payment records for re-listings
- Updates Property status and plan fields
- Maintains payment history

## Files Modified

1. ✅ `core/views.py` - Updated select_plan_view() and payment_view()

## Status

✅ **Fix Applied and Tested**
✅ **No Syntax Errors**
✅ **Django Check Passed**
✅ **Ready to Use**

---

**Fixed:** March 14, 2026
**Issue:** Re-list button not working
**Solution:** Added is_relisting checks to bypass payment validation
**Result:** Re-listing feature now fully functional
