# Quick Start Guide - Razorpay Payment Setup

## ⚡ 5-Minute Setup

### Step 1: Get Razorpay Account (2 minutes)
1. Go to https://razorpay.com/
2. Click "Sign Up"
3. Complete registration
4. Verify email

### Step 2: Get API Keys (2 minutes)
1. Login to Razorpay Dashboard
2. Go to **Settings** → **API Keys**
3. Copy these two values:
   - **Key ID** (Example: `rzp_test_L7v9nM8kX5pQ2r`)
   - **Key Secret** (Example: `7z9X2k5mP8v3L1q4`)

### Step 3: Update Settings (1 minute)

Edit: `HomeRentalManagement/settings.py`

Find these lines:
```python
RAZORPAY_KEY_ID = 'rzp_test_YOUR_KEY_ID'
RAZORPAY_KEY_SECRET = 'rzp_test_YOUR_KEY_SECRET'
```

Replace with your keys:
```python
RAZORPAY_KEY_ID = 'rzp_test_L7v9nM8kX5pQ2r'
RAZORPAY_KEY_SECRET = '7z9X2k5mP8v3L1q4'
```

### Done! ✅

---

## 🧪 Test the Payment

### 1. Start Server
```bash
python manage.py runserver
```

### 2. Register as Owner
- Go to http://127.0.0.1:8000/register/
- Create account with role "Owner"
- Login

### 3. Add Property
- Click "Add Property"
- Fill details
- Upload photos
- Click "Pay Now"

### 4. Complete Test Payment
- Card Number: `4111 1111 1111 1111`
- Expiry: `12/25`
- CVV: `123`
- Click "Pay"

### 5. Verify Success
- You'll see success message
- Check admin panel at http://127.0.0.1:8000/admin/
- Go to **Core** → **Payments**
- Your payment should show as "SUCCESS"

---

## 🔍 Check Payment Status

### In Admin Panel:
1. Go to http://127.0.0.1:8000/admin/
2. Login (admin/admin123)
3. Click **Core** → **Payments**
4. See all property registration payments
5. Filter by status or search by property name

### In Database:
```python
from core.models import Payment

# Get all successful payments
successful = Payment.objects.filter(status='SUCCESS')

# Get specific property payment
payment = Payment.objects.get(property_id=1)
print(payment.razorpay_payment_id)
print(payment.razorpay_order_id)
print(payment.amount)
```

---

## 📊 Payment Flow

```
Owner Registration
      ↓
Add Property + Photos
      ↓
Redirect to Payment Page
      ↓
Click "Pay ₹100 with Razorpay"
      ↓
Razorpay Checkout Opens
      ↓
Owner Completes Payment
      ↓
Backend Verifies Signature
      ↓
Property Marked as Paid
      ↓
Sent for Admin Approval
      ↓
Admin Approves/Rejects
      ↓
Property Listed or Rejected
```

---

## 💳 Test Cards Available

### Visa
- Number: `4111 1111 1111 1111`
- Expiry: Any future date
- CVV: Any 3 digits

### Mastercard
- Number: `5555 5555 5555 4444`
- Expiry: Any future date
- CVV: Any 3 digits

### Amex
- Number: `3782 822463 10005`
- Expiry: Any future date
- CVV: Any 4 digits

**Note**: Use these only for testing. They don't charge real money.

---

## 🚀 Go Live Checklist

When ready for production:

- [ ] Get live Razorpay account
- [ ] Replace test keys with live keys:
  ```python
  RAZORPAY_KEY_ID = 'rzp_live_YOUR_LIVE_KEY'
  RAZORPAY_KEY_SECRET = 'rzp_live_YOUR_LIVE_SECRET'
  ```
- [ ] Set `DEBUG = False`
- [ ] Update `ALLOWED_HOSTS` with your domain
- [ ] Use HTTPS (required for Razorpay)
- [ ] Test with real payment
- [ ] Monitor payments in Razorpay dashboard

---

## ❓ FAQ

**Q: Will I be charged for test payments?**
A: No! Test card numbers never charge real money.

**Q: How do I see payment history?**
A: Login to Razorpay dashboard or check `/admin/core/payment/`

**Q: What if payment fails?**
A: Error message shows on page. You can retry. Database tracks failed attempts.

**Q: Can I change the fee?**
A: Yes! Edit `PROPERTY_REGISTRATION_FEE` in settings.py

**Q: Is it secure?**
A: Yes! Razorpay is PCI-DSS certified. We verify signatures server-side.

**Q: What payment methods work?**
A: Cards, UPI, Wallets (PayTM, Google Pay, Apple Pay, etc.), Net Banking

**Q: How long does refund take?**
A: 3-5 business days (depends on bank)

---

## 📞 Support

- **Razorpay Support**: https://razorpay.com/support/
- **Integration Issues**: Check RAZORPAY_SETUP.md
- **Technical Details**: See TECHNICAL_DETAILS.md

---

## ✨ Features Included

✅ Secure Razorpay integration  
✅ Server-side signature verification  
✅ Payment tracking in database  
✅ Admin panel for payments  
✅ Beautiful payment UI  
✅ Real-time payment status  
✅ Error handling & logging  
✅ Support for multiple payment methods  

---

**Ready to accept payments?** You're all set! 🎉
