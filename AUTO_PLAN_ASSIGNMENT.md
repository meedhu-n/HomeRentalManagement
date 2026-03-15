# Automatic Plan Assignment - No Repeat Payment Required

## Feature Overview
Owners with active Premium or Standard plans no longer need to pay again when adding additional properties within their plan limits. The system automatically assigns new properties to their existing plan.

## How It Works

### Plan Limits
- **Basic Plan**: 1 property
- **Standard Plan**: 3 properties
- **Premium Plan**: 10 properties

### Automatic Assignment Logic

When an owner adds a new property and reaches the "Select Plan" page, the system:

1. **Checks for Active Plans**
   - Looks for properties with `is_paid=True` and `plan_expiry_date > now()`
   - Counts properties by plan type (Premium, Standard, Basic)

2. **Determines Available Slots**
   - Premium: If owner has < 10 active properties with premium plan
   - Standard: If owner has < 3 active properties with standard plan
   - Basic: Always requires new payment (1 property limit)

3. **Auto-Assigns Property**
   - If slots are available, the new property is automatically:
     - Marked as `is_paid=True`
     - Assigned the same `plan_type` as existing plan
     - Given the same `plan_expiry_date` as the earliest expiring property in that plan
     - Set to `PENDING_APPROVAL` status
   - Owner is redirected to dashboard with success message
   - **No payment page is shown**

4. **Requires Payment When**
   - Owner has no active plans
   - Owner has reached their plan limit
   - Property is being re-listed (rented properties)

## Example Scenarios

### Scenario 1: Premium Plan Owner (3 properties)
- Owner has 3 active properties with Premium plan
- Adds a 4th property
- System auto-assigns to Premium plan (no payment)
- Property goes to pending approval
- Owner can add up to 10 properties total

### Scenario 2: Standard Plan Owner (3 properties - at limit)
- Owner has 3 active properties with Standard plan
- Tries to add a 4th property
- System shows plan selection page
- Owner must purchase a new plan or upgrade to Premium

### Scenario 3: Mixed Plans
- Owner has 1 Premium property and 2 Basic properties (3 total)
- Adds a new property
- System uses Premium plan (allows up to 10)
- New property auto-assigned to Premium plan

### Scenario 4: Re-listing Rented Property
- Owner has a rented property they want to re-list
- Even if they have available slots, they must pay again
- This is because the property needs a fresh listing period

## Benefits

✅ **No Repeat Payments**: Owners don't pay multiple times for the same plan period
✅ **Seamless Experience**: Properties are automatically assigned to existing plans
✅ **Fair Usage**: Plan limits are properly enforced
✅ **Expiry Alignment**: All properties under the same plan expire together
✅ **Cost Effective**: Owners get full value from their Premium/Standard plans

## Technical Implementation

### Modified Function
- `select_plan_view()` in `core/views.py`

### Key Logic
```python
# Check if owner has active plan with available slots
active_properties = Property.objects.filter(
    owner=request.user,
    is_paid=True,
    plan_expiry_date__gt=timezone.now()
).exclude(id=property_obj.id)

# Check Premium plan (allows up to 10 properties)
if premium_count > 0 and total_active < 10:
    can_use_existing_plan = True
    existing_plan_type = 'premium'
    existing_plan_expiry = premium_properties.order_by('plan_expiry_date').first().plan_expiry_date

# Auto-assign if eligible
if can_use_existing_plan and not is_relisting:
    property_obj.is_paid = True
    property_obj.plan_type = existing_plan_type
    property_obj.plan_expiry_date = existing_plan_expiry
    property_obj.status = Property.Status.PENDING_APPROVAL
    property_obj.save()
    # Redirect to dashboard (skip payment)
```

### Plan Expiry Strategy
- New properties inherit the **earliest expiry date** from existing properties in the same plan
- This ensures all properties in a plan expire together
- Prevents confusion about different expiry dates

## User Experience Flow

### With Available Slots (No Payment)
1. Owner clicks "Add Property"
2. Fills property details
3. Uploads photos
4. Sets location
5. Reaches "Select Plan" page
6. **System auto-assigns to existing plan**
7. Success message: "Property added to your existing Premium Plan! No payment required."
8. Redirected to dashboard
9. Property shows as "Pending Approval"

### Without Available Slots (Payment Required)
1. Owner clicks "Add Property"
2. Fills property details
3. Uploads photos
4. Sets location
5. Reaches "Select Plan" page
6. Selects a plan (Basic/Standard/Premium)
7. Proceeds to payment page
8. Completes payment
9. Property goes to pending approval

## Files Modified
- `core/views.py` - Updated `select_plan_view()` function

## Testing Checklist
- [ ] Owner with Premium plan (< 10 properties) adds new property - no payment required
- [ ] Owner with Standard plan (< 3 properties) adds new property - no payment required
- [ ] Owner with Basic plan tries to add 2nd property - payment required
- [ ] Owner at plan limit tries to add property - payment required
- [ ] Owner re-listing rented property - payment required
- [ ] New property gets correct plan_type and plan_expiry_date
- [ ] New property goes to PENDING_APPROVAL status
- [ ] Success message displays correctly
