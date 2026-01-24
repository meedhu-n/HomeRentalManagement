# 🔑 How to Get Razorpay API Keys (2 Minutes)

## Step 1: Create Free Razorpay Account

1. Go to **https://razorpay.com**
2. Click **"Sign Up"** (top right)
3. Enter your email
4. Create a password
5. Click **"Sign Up"**

## Step 2: Verify Your Email

1. Check your email inbox
2. Click the verification link from Razorpay
3. You'll be redirected to complete your account

## Step 3: Complete Account Setup

1. Fill in your business details:
   - Business name (e.g., "My Property Rental")
   - Business type: Select **"Education/E-Learning"** or **"Real Estate"**
   - Phone number
   - Address

2. Click **"Create Account"**

## Step 4: Get Your API Keys

1. Login to **https://dashboard.razorpay.com**
2. Go to **Settings** (left sidebar)
3. Click **API Keys**
4. You'll see two sections:

### Test Keys (For Development - Use These First!)
```
Key ID:     rzp_test_XXXXXXXXXXXXX
Key Secret: XXXXXXXXXXXXXXXXXXXXXX
```

5. **Copy both values**

## Step 5: Add Keys to Django Settings

1. Open: `config/settings.py`
2. Find these lines:
```python
RAZORPAY_KEY_ID = 'rzp_test_YOUR_KEY_ID'
RAZORPAY_KEY_SECRET = 'rzp_test_YOUR_KEY_SECRET'
```

3. Replace with your copied keys:
```python
RAZORPAY_KEY_ID = 'rzp_test_XXXXXXXXXXXXX'
RAZORPAY_KEY_SECRET = 'XXXXXXXXXXXXXXXXXXXXXX'
```

4. **Save the file**

## Step 6: Reload Django Server

1. Stop the server (Ctrl+C)
2. Start it again:
```bash
python manage.py runserver
```

## Step 7: Test Payment

1. Go to http://127.0.0.1:8000/register
2. Create owner account
3. Add property + photos
4. Click "Pay ₹100"
5. Use test card: **4111 1111 1111 1111**
6. Expiry: Any future date (12/25)
7. CVV: Any 3 digits (123)

## ✅ Done!

You're all set to accept payments!

---

## 📝 Important Notes

### Test vs Live Keys
- **Test Keys**: Don't charge real money, safe to test
- **Live Keys**: Charge real money, use only in production

### Where to Find Keys Again
- Login: https://dashboard.razorpay.com
- Path: Settings → API Keys

### Don't Share Your Keys!
- Keep `RAZORPAY_KEY_SECRET` secret
- Never commit to public GitHub
- Use environment variables in production

---

## 🆘 Troubleshooting

**Still getting "Authentication failed"?**
- Clear browser cache (Ctrl+Shift+Delete)
- Restart Django server
- Double-check you copied the KEY ID (not KEY SECRET)

**Keys not working?**
- Make sure they're "Test" keys (start with `rzp_test_`)
- Verify exact copy-paste (no extra spaces)
- Check Razorpay dashboard hasn't been suspended

**Can't login to Razorpay?**
- Go to: https://dashboard.razorpay.com/signin
- Use email you signed up with
- Click "Forgot password" if needed

---

## 🎯 Next Steps

1. ✅ Get Razorpay account (5 min)
2. ✅ Get API keys (1 min)
3. ✅ Update settings.py (1 min)
4. ✅ Test payment (2 min)
5. ✅ Go live (when ready)

**Total Time**: 10 minutes to start accepting payments!
