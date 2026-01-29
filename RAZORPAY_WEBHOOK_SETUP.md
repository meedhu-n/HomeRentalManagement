# Razorpay Webhook Setup Guide

## What are Webhooks?

Webhooks allow Razorpay to notify your application automatically when payment events occur (success, failure, etc.). This is more reliable than frontend-only verification.

## Benefits of Using Webhooks:

✅ **Automatic payment confirmation** - No manual verification needed
✅ **More reliable** - Works even if user closes browser
✅ **Real-time updates** - Instant notification of payment status
✅ **Better security** - Server-side verification

---

## Setup Instructions

### Step 1: Expose Your Local Server (For Testing)

Since webhooks need a public URL, you need to expose your local server using **ngrok**:

1. **Download ngrok:**
   - Visit: https://ngrok.com/download
   - Download and extract ngrok

2. **Run ngrok:**
   ```bash
   ngrok http 8000
   ```

3. **Copy the HTTPS URL:**
   - You'll see something like: `https://abc123.ngrok.io`
   - Copy this URL

### Step 2: Configure Webhook in Razorpay Dashboard

1. **Go to Razorpay Dashboard:**
   - Visit: https://dashboard.razorpay.com/app/webhooks

2. **Create New Webhook:**
   - Click **"Add New Webhook"** or **"Create Webhook"**

3. **Enter Webhook URL:**
   ```
   https://your-ngrok-url.ngrok.io/razorpay-webhook/
   ```
   Example: `https://abc123.ngrok.io/razorpay-webhook/`

4. **Select Events to Listen:**
   - ✅ `payment.captured` (Payment successful)
   - ✅ `payment.failed` (Payment failed)
   - ✅ `order.paid` (Order completed)

5. **Set Alert Email (Optional):**
   - Add your email for webhook failure notifications

6. **Save Webhook:**
   - Click **"Create Webhook"** or **"Save"**

7. **Copy Webhook Secret:**
   - After creating, you'll see a **Webhook Secret**
   - Copy this secret key

### Step 3: Add Webhook Secret to Your Project

1. **Open:** `config/settings.py`

2. **Update the webhook secret:**
   ```python
   RAZORPAY_WEBHOOK_SECRET = 'your_webhook_secret_here'
   ```

3. **Save the file** (Django will auto-reload)

---

## Testing Webhooks

### Method 1: Make a Real Payment

1. Start your Django server: `python manage.py runserver`
2. Start ngrok: `ngrok http 8000`
3. Make a test payment using test card: `4111 1111 1111 1111`
4. Check your server logs - you should see webhook events

### Method 2: Test from Razorpay Dashboard

1. Go to: https://dashboard.razorpay.com/app/webhooks
2. Click on your webhook
3. Click **"Send Test Webhook"**
4. Select event type: `payment.captured`
5. Click **"Send"**

---

## Webhook URL Format

Your webhook URL should be:
```
https://your-domain.com/razorpay-webhook/
```

For local testing with ngrok:
```
https://abc123.ngrok.io/razorpay-webhook/
```

For production:
```
https://yourdomain.com/razorpay-webhook/
```

---

## How It Works

1. **User makes payment** → Razorpay processes it
2. **Razorpay sends webhook** → To your `/razorpay-webhook/` endpoint
3. **Your server receives webhook** → Verifies and updates payment status
4. **Property marked as paid** → Automatically in database

---

## Troubleshooting

### Webhook not receiving events?

1. **Check ngrok is running:**
   ```bash
   ngrok http 8000
   ```

2. **Verify webhook URL in Razorpay:**
   - Should end with `/razorpay-webhook/`
   - Should use HTTPS (ngrok provides this)

3. **Check server logs:**
   - Look for "Webhook received" messages
   - Check for any errors

### Payment not updating?

1. **Check webhook events are enabled:**
   - `payment.captured` should be checked
   
2. **Verify order_id matches:**
   - Check server logs for order_id

3. **Check database:**
   - Go to Django admin: http://127.0.0.1:8000/admin/
   - Check Payments table

---

## Production Deployment

For production (not localhost):

1. **Use your actual domain:**
   ```
   https://yourdomain.com/razorpay-webhook/
   ```

2. **Enable webhook signature verification:**
   - Add webhook secret to settings
   - Uncomment verification code in `views.py`

3. **Use HTTPS:**
   - Razorpay requires HTTPS for webhooks
   - Use SSL certificate on your domain

---

## Current Implementation Status

✅ Webhook endpoint created: `/razorpay-webhook/`
✅ Handles `payment.captured` event
✅ Handles `payment.failed` event
✅ Auto-updates payment status
✅ Auto-marks property as paid

⏳ **Next Step:** Configure webhook URL in Razorpay dashboard

---

## Quick Start (Local Testing)

```bash
# Terminal 1: Start Django
python manage.py runserver

# Terminal 2: Start ngrok
ngrok http 8000

# Copy the ngrok HTTPS URL
# Add to Razorpay dashboard: https://your-ngrok-url.ngrok.io/razorpay-webhook/
```

---

## Need Help?

- Razorpay Webhook Docs: https://razorpay.com/docs/webhooks/
- ngrok Setup: https://ngrok.com/docs/getting-started/
