# Rejected Property Edit & Resubmit Feature

## Overview
Owners can now edit rejected properties and resubmit them for admin approval. This allows owners to fix issues mentioned in the rejection reason and get their properties approved without creating a new listing.

## Features Implemented

### 1. Edit & Resubmit Button
Added to rejected properties section in owner dashboard:
- Prominent "Edit & Resubmit" button alongside "Delete" button
- Clear visual indication that property can be edited
- Maintains existing property data and payment information

### 2. Edit Flow for Rejected Properties
New view: `edit_rejected_property_view()`
- Validates property is in REJECTED status
- Stores rejection reason in session for reference
- Allows owner to update property details
- Maintains payment and plan information

### 3. Seamless Workflow
The complete flow for editing and resubmitting:
1. Owner sees rejected property with rejection reason
2. Clicks "Edit & Resubmit" button
3. Redirected to property edit form (with rejection reason displayed)
4. Updates property details
5. Updates photos (optional - can keep existing)
6. Updates location (optional)
7. Reaches plan selection page
8. System automatically resubmits without payment (if already paid)
9. Property status changes to PENDING_APPROVAL
10. Rejection reason is cleared
11. Owner redirected to dashboard with success message

### 4. Smart Payment Handling
The system intelligently handles payment:
- If property was already paid for, no new payment required
- If owner has active Premium/Standard plan with slots, uses existing plan
- Property maintains its original plan type and expiry date
- No duplicate payments for the same property

## Technical Implementation

### New View: `edit_rejected_property_view()`
```python
@login_required
def edit_rejected_property_view(request, id):
    """Edit a rejected property and resubmit for approval"""
    property_obj = get_object_or_404(Property, id=id, owner=request.user)
    
    # Ensure property is actually rejected
    if property_obj.status != Property.Status.REJECTED:
        messages.error(request, "This property is not in rejected status.")
        return redirect('dashboard')
    
    # Store rejection info in session
    request.session['editing_rejected_property'] = True
    request.session['rejection_reason'] = property_obj.rejection_reason
    request.session['rejected_property_id'] = property_obj.id
    
    # Continue with edit flow...
```

### Updated Views

#### `add_photos_view()`
- Now checks for `is_rejected_edit` flag
- Allows using existing photos without uploading new ones
- Continues to location page

#### `select_plan_view()`
- Detects rejected property resubmission
- If already paid, automatically resubmits without payment
- Clears rejection reason
- Changes status to PENDING_APPROVAL
- Clears session flags

### URL Added
```python
path('edit-rejected-property/<int:id>/', views.edit_rejected_property_view, name='edit_rejected_property')
```

### Owner Dashboard Update
```html
<div style="display: flex; gap: 10px; flex-wrap: wrap;">
    <a href="{% url 'edit_rejected_property' property.id %}" class="btn-manage">
        <i class="fas fa-edit"></i>
        Edit & Resubmit
    </a>
    <a href="{% url 'delete_property' property.id %}" class="btn-manage">
        <i class="fas fa-trash"></i>
        Delete
    </a>
</div>
```

## User Experience Flow

### Owner's Perspective

1. **Receives Rejection Notification**
   - Email notification with rejection reason
   - Property appears in "Rejected Properties" section

2. **Reviews Rejection Reason**
   - Clear display of why property was rejected
   - Highlighted rejection reason box with icon

3. **Edits Property**
   - Clicks "Edit & Resubmit" button
   - Sees rejection reason as reminder
   - Updates property details to address issues

4. **Updates Photos (Optional)**
   - Can upload new photos
   - Can keep existing photos
   - Flexibility to fix photo-related issues

5. **Updates Location (Optional)**
   - Can update map location
   - Can skip if location was correct

6. **Automatic Resubmission**
   - No payment required (already paid)
   - Property automatically resubmitted
   - Status changes to PENDING_APPROVAL
   - Success message confirms resubmission

7. **Waits for Approval**
   - Property moves from "Rejected" to "Active Listings"
   - Shows "Pending Approval" status
   - Receives notification when approved/rejected

### Admin's Perspective

1. **Sees Resubmitted Property**
   - Property appears in "Pending Approvals" section
   - Can see it was previously rejected (if needed)
   - Reviews updated property details

2. **Makes Decision**
   - Approves if issues are fixed
   - Rejects again with new reason if still problematic

## Benefits

### For Owners
✅ No need to create new listing from scratch
✅ Maintains payment and plan information
✅ No duplicate payments
✅ Clear guidance on what needs fixing
✅ Simple, streamlined process
✅ Preserves property history and images

### For Admins
✅ Owners fix issues instead of creating duplicates
✅ Better quality control
✅ Reduced workload (fewer duplicate listings)
✅ Clear communication through rejection reasons

### For System
✅ Maintains data integrity
✅ No orphaned payment records
✅ Clean property lifecycle management
✅ Efficient use of database resources

## Edge Cases Handled

### 1. Property Not Rejected
If owner tries to edit a non-rejected property through this flow:
- Error message displayed
- Redirected to dashboard

### 2. Already Paid Property
If property was already paid for:
- No payment page shown
- Automatically resubmitted
- Plan information maintained

### 3. Active Plan Available
If owner has active Premium/Standard plan with slots:
- Property uses existing plan
- No payment required
- Expiry date aligned with existing plan

### 4. Session Management
- Session flags properly set and cleared
- No conflicts with re-listing flow
- Clean state after resubmission

## Files Modified

1. **core/views.py**
   - Added `edit_rejected_property_view()`
   - Updated `add_photos_view()` to handle rejected edits
   - Updated `select_plan_view()` to handle resubmission

2. **core/urls.py**
   - Added URL for `edit_rejected_property`

3. **core/templates/core/owner_dashboard.html**
   - Added "Edit & Resubmit" button
   - Updated button layout for rejected properties

## Testing Checklist

- [ ] Rejected property shows "Edit & Resubmit" button
- [ ] Click button redirects to edit form
- [ ] Rejection reason is displayed as info message
- [ ] Can update property details
- [ ] Can update photos (or keep existing)
- [ ] Can update location (or skip)
- [ ] Reaches plan selection page
- [ ] If already paid, automatically resubmits
- [ ] Property status changes to PENDING_APPROVAL
- [ ] Rejection reason is cleared
- [ ] Success message displays
- [ ] Property moves to active listings section
- [ ] Admin sees property in pending approvals
- [ ] Session flags are properly cleared
- [ ] No payment required for resubmission
- [ ] Works with active plan slots

## Future Enhancements

### Possible Improvements
1. Track rejection/resubmission history
2. Show number of times property was rejected
3. Add rejection categories for better tracking
4. Allow admin to see previous rejection reasons
5. Add analytics on common rejection reasons
6. Implement auto-suggestions based on rejection reason

## Related Features
- Property Rejection System
- Payment System
- Plan Management
- Email Notifications
- Owner Dashboard

## Database Changes
No new migrations required. Uses existing fields:
- `Property.status` - Changes from REJECTED to PENDING_APPROVAL
- `Property.rejection_reason` - Cleared on resubmission
- `Property.is_paid` - Maintained
- `Property.plan_type` - Maintained
- `Property.plan_expiry_date` - Maintained
