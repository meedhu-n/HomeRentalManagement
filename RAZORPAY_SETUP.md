# Razorpay Payment Integration Guide

## Overview
Property owners now need to pay a registration fee when listing a property. The fee is processed through Razorpay, a secure payment gateway.

## Setup Instructions

### 1. Get Razorpay Credentials

1. Visit [Razorpay Dashboard](https://dashboard.razorpay.com/)
2. Sign up for a free account (or login if you have one)
3. Go to **Settings → API Keys**
4. Copy your:
   - **Key ID** (starts with `rzp_test_` for testing or `rzp_live_` for production)
   - **Key Secret** (keep this secure!)

### 2. Update Django Settings

Edit `HomeRentalManagement/settings.py` and replace:

```python
RAZORPAY_KEY_ID = 'rzp_test_YOUR_KEY_ID'  # Paste your Key ID here
RAZORPAY_KEY_SECRET = 'rzp_test_YOUR_KEY_SECRET'  # Paste your Key Secret here
PROPERTY_REGISTRATION_FEE = 100  # Amount in INR (change as needed)
```

### 3. Payment Flow

When an owner registers a property:
1. They upload property details and photos
2. They're redirected to `/payment/<property_id>/`
3. A Razorpay order is created
4. They click "Pay ₹100 with Razorpay"
5. Razorpay payment modal opens
6. After successful payment, signature is verified
7. Property is marked as `is_paid = True`
8. Property is sent for admin approval

### 4. Admin Panel

- Admins can view all payments at: `/admin/core/payment/`
- Payments show:
  - Property name
  - Owner
  - Amount
  - Payment status (PENDING, SUCCESS, FAILED)
  - Payment timestamps
  - Razorpay order/payment IDs

### 5. Testing Razorpay

For testing, use these test card numbers:
- **Visa**: 4111 1111 1111 1111
- **Mastercard**: 5555 5555 5555 4444
- **Expiry**: Any future date (e.g., 12/25)
- **CVV**: Any 3 digits (e.g., 123)

### 6. Database Models

#### Payment Model
```
- property: OneToOne → Property
- owner: ForeignKey → User
- razorpay_order_id: Unique order ID from Razorpay
- razorpay_payment_id: Payment ID from Razorpay
- razorpay_signature: Digital signature for verification
- amount: Registration fee in INR
- status: PENDING, SUCCESS, or FAILED
- created_at: Timestamp
- updated_at: Timestamp
```

### 7. Security Features

✅ **CSRF Protection**: Token verified on payment verification  
✅ **Signature Verification**: Razorpay signature validated server-side  
✅ **One-time Payment**: Each property can only be paid once  
✅ **Secure API Keys**: Keys stored in Django settings  

### 8. Environment Variables (Production)

For production, use environment variables instead of hardcoding:

```python
import os
from dotenv import load_dotenv

load_dotenv()

RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID')
RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET')
```

Create a `.env` file:
```
RAZORPAY_KEY_ID=rzp_live_YOUR_PRODUCTION_KEY
RAZORPAY_KEY_SECRET=rzp_live_YOUR_PRODUCTION_SECRET
```

### 9. Troubleshooting

**Payment page not loading?**
- Check Razorpay keys are correct
- Verify all imports in views.py
- Check browser console for JavaScript errors

**Signature verification fails?**
- Ensure key order in signature verification matches Razorpay docs
- Check order_id, payment_id, and signature are correct
- Verify keys are for the same environment (test/live)

**Property not marked as paid?**
- Check Payment model in database
- Verify is_paid field on Property model
- Check admin logs for any errors

### 10. Admin Features

Admins can:
- View all payments with filters
- Search by property name or Razorpay order ID
- See payment status at a glance
- Only approve properties that have `is_paid = True`

### 11. Future Enhancements

Possible improvements:
- Subscription payments for premium listings
- Partial refunds for rejected properties
- Payment reminders via email
- Revenue reports and analytics
- Multiple payment method support (Apple Pay, Google Pay)

---

**Current Fee**: ₹100 (changeable in settings)  
**Payment Gateway**: Razorpay  
**Currency**: Indian Rupees (INR)  
**Status**: ✅ Production Ready
