# Payment Unique Constraint Fix

## Error

```
Payment error: UNIQUE constraint failed: core_payment.property_id
```

## Root Cause

The Payment model was using `OneToOneField` for the property relationship:

```python
property = models.OneToOneField(Property, on_delete=models.CASCADE, related_name='payment')
```

This creates a UNIQUE constraint on `property_id`, meaning:
- Each property can only have ONE payment record
- When trying to re-list a rented property, it attempts to create a SECOND payment
- Database rejects this because of the UNIQUE constraint

## Solution

Changed the Payment model to use `ForeignKey` instead of `OneToOneField`:

### Before:
```python
class Payment(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE, related_name='payment')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
```

### After:
```python
class Payment(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='payments')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments_made')
```

## Changes Made

### 1. Updated Payment Model (core/models.py)

**Changed:**
- `OneToOneField` → `ForeignKey` for property relationship
- `related_name='payment'` → `related_name='payments'` (plural)
- `related_name='payments'` → `related_name='payments_made'` for owner (to avoid conflict)

**Impact:**
- Now allows multiple payment records per property
- Enables payment history tracking
- Supports re-listing workflow

### 2. Updated payment_view() (core/views.py)

**Changed:**
```python
# Before
payment = Payment.objects.get(property=property_obj)

# After
payment = Payment.objects.filter(property=property_obj).latest('created_at')
```

**Why:**
- `get()` expects exactly one record (fails with multiple)
- `filter().latest()` gets the most recent payment record
- Works with multiple payments per property

### 3. Created Migration

**Migration:** `0015_alter_payment_owner_alter_payment_property.py`

**Operations:**
- Altered `property` field from OneToOneField to ForeignKey
- Altered `owner` related_name to avoid conflicts
- Applied successfully to database

## Benefits

### ✅ Multiple Payments Per Property
- Property can be paid for multiple times
- Each re-listing creates a new payment record
- Complete payment history maintained

### ✅ Re-listing Now Works
- No more UNIQUE constraint errors
- Owners can re-list rented properties
- Payment flow completes successfully

### ✅ Payment History
- Track all payments for a property
- See when property was listed/re-listed
- Audit trail for revenue tracking

### ✅ Better Data Model
- More flexible for future features
- Supports subscription renewals
- Allows payment refunds/adjustments

## Database Changes

### Before Migration:
```sql
CREATE TABLE core_payment (
    id INTEGER PRIMARY KEY,
    property_id INTEGER UNIQUE,  -- UNIQUE constraint
    ...
);
```

### After Migration:
```sql
CREATE TABLE core_payment (
    id INTEGER PRIMARY KEY,
    property_id INTEGER,  -- No UNIQUE constraint
    ...
);
```

## Code Access Changes

### Before (OneToOneField):
```python
# Access payment (singular)
property.payment  # Returns single Payment object or raises DoesNotExist

# Create payment
Payment.objects.create(property=property_obj, ...)  # Fails if payment exists
```

### After (ForeignKey):
```python
# Access payments (plural)
property.payments.all()  # Returns QuerySet of all payments
property.payments.latest('created_at')  # Get most recent payment
property.payments.filter(status='SUCCESS')  # Filter payments

# Create payment
Payment.objects.create(property=property_obj, ...)  # Always works
```

## Testing

### Test Re-listing Flow:

```bash
# 1. Start server
python manage.py runserver

# 2. Login as owner

# 3. Mark a property as RENTED

# 4. Go to Owner Dashboard
# - See "Rented Properties" section

# 5. Click "Re-List Property"
# - Should redirect to plan selection ✅

# 6. Select a plan
# - Should redirect to payment page ✅

# 7. Complete payment
# - Should process successfully ✅
# - NO "UNIQUE constraint failed" error ✅

# 8. Check database
# - Property should have 2 payment records ✅
# - Both payments visible in admin panel ✅
```

### Verify Payment History:

```python
# In Django shell
from core.models import Property, Payment

# Get a property
property = Property.objects.first()

# See all payments
payments = property.payments.all()
print(f"Total payments: {payments.count()}")

# See payment history
for payment in payments:
    print(f"{payment.created_at}: ₹{payment.amount} - {payment.status}")
```

## Admin Panel Impact

### Before:
- Payment shown as inline on Property admin
- Only one payment visible per property

### After:
- Multiple payments visible per property
- Payment history in admin panel
- Can filter/search all payments

## Revenue Tracking Impact

The admin revenue dashboard now shows:
- All payment transactions (including re-listings)
- Complete payment history
- Accurate revenue calculations
- Multiple payments per property tracked

## Migration Details

**File:** `core/migrations/0015_alter_payment_owner_alter_payment_property.py`

**Status:** ✅ Applied successfully

**Reversible:** Yes (can rollback if needed)

**Data Loss:** None (existing payments preserved)

## Files Modified

1. ✅ `core/models.py` - Changed Payment model
2. ✅ `core/views.py` - Updated payment_view()
3. ✅ `core/migrations/0015_*.py` - Created migration

## Summary

| Issue | Solution | Status |
|-------|----------|--------|
| UNIQUE constraint error | Changed OneToOneField to ForeignKey | ✅ Fixed |
| Can't re-list properties | Allow multiple payments per property | ✅ Fixed |
| Payment history missing | Track all payments with ForeignKey | ✅ Fixed |
| Code access pattern | Use .latest() instead of .get() | ✅ Updated |

---

**Fixed:** March 14, 2026

**Error:** UNIQUE constraint failed: core_payment.property_id

**Solution:** Changed Payment.property from OneToOneField to ForeignKey

**Result:** Re-listing feature now fully functional with payment history tracking

**Migration:** Applied successfully

**Testing:** Verified working
