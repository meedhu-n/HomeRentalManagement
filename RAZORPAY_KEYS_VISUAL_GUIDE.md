# 🎯 Razorpay Dashboard - Visual Guide

## Quick Path to API Keys

```
https://dashboard.razorpay.com
         ↓
    [LOGIN with email & password]
         ↓
    Left Sidebar → SETTINGS
         ↓
    Settings Page → API KEYS
         ↓
    Copy TWO values:
    • Key ID (starts with rzp_test_)
    • Key Secret (long random string)
```

## Razorpay Dashboard Layout

```
┌─────────────────────────────────────────────┐
│  RAZORPAY DASHBOARD                         │
├─────────────────────────────────────────────┤
│  [LOGO] [Search]  [Profile] [Settings] [?]  │
├─────────────────────────────────────────────┤
│ ├─ Overview                                  │
│ ├─ Transactions                              │
│ ├─ Orders                                    │
│ ├─ Payouts                                   │
│ ├─ Invoices                                  │
│ ├─ Customers                                 │
│ ├─ Reports                                   │
│ ├─ SETTINGS ← CLICK HERE                     │
│ └─ Help                                      │
└─────────────────────────────────────────────┘
```

## Inside Settings

```
┌─────────────────────────────────────────────┐
│  SETTINGS                                   │
├─────────────────────────────────────────────┤
│ ├─ Account                                   │
│ ├─ Billing                                   │
│ ├─ API Keys ← CLICK HERE                     │
│ ├─ Webhooks                                  │
│ ├─ Smart Routing                             │
│ ├─ Team & Access                             │
│ └─ Brand Details                             │
└─────────────────────────────────────────────┘
```

## API Keys Page

```
┌─────────────────────────────────────────────┐
│  API KEYS                                   │
├─────────────────────────────────────────────┤
│                                              │
│ 🔓 TEST KEYS (Use for development)          │
│                                              │
│ Key ID:                                     │
│ ┌─────────────────────────────────────────┐ │
│ │ rzp_test_XXXXXXXXXXXXX          [COPY] │ │
│ └─────────────────────────────────────────┘ │
│                                              │
│ Key Secret:                                 │
│ ┌─────────────────────────────────────────┐ │
│ │ XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  │ │
│ │ XXXXXXXXXXXXXXXXXXXX          [COPY] │ │
│ └─────────────────────────────────────────┘ │
│                                              │
│ ════════════════════════════════════════    │
│                                              │
│ 🔒 LIVE KEYS (Use in production)            │
│    [Verify your business to unlock]         │
│                                              │
└─────────────────────────────────────────────┘
```

## Exactly What You Need to Copy

### Test Key ID
```
rzp_test_XXXXXXXXXXXXX
```
- **Starts with**: rzp_test_
- **Length**: ~20 characters
- **Where to paste**: RAZORPAY_KEY_ID in settings.py

### Test Key Secret
```
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```
- **Starts with**: Random characters (no rzp_ prefix)
- **Length**: ~40 characters
- **Where to paste**: RAZORPAY_KEY_SECRET in settings.py

---

## Step-by-Step with Screenshots Locations

| Step | Action | Location |
|------|--------|----------|
| 1 | Go to Razorpay | https://razorpay.com |
| 2 | Sign Up | Top right button |
| 3 | Verify Email | Check your inbox |
| 4 | Login | https://dashboard.razorpay.com |
| 5 | Click Settings | Left sidebar menu |
| 6 | Click API Keys | Settings submenu |
| 7 | Copy Key ID | Blue COPY button next to Key ID |
| 8 | Copy Key Secret | Blue COPY button next to Key Secret |
| 9 | Open settings.py | `config/settings.py` |
| 10 | Update RAZORPAY_KEY_ID | Paste the Key ID |
| 11 | Update RAZORPAY_KEY_SECRET | Paste the Key Secret |
| 12 | Save file | Ctrl+S |
| 13 | Restart server | Stop and restart runserver |

---

## What NOT to Do

❌ **Don't share your Key Secret** - Keep it private!  
❌ **Don't use live keys yet** - Stick with test keys for now  
❌ **Don't commit to GitHub** - It will be public!  
❌ **Don't leave placeholder values** - Update them completely  

---

## Verification

After updating settings.py, verify your keys are loaded:

```bash
python manage.py shell
>>> from django.conf import settings
>>> print(settings.RAZORPAY_KEY_ID)
rzp_test_XXXXXXXXXXXXX  # Should print your Key ID

>>> print(settings.RAZORPAY_KEY_SECRET)
XXXXXXXXXXXXXXXXXXXXXX  # Should print your Key Secret (partial)
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Copied Key Secret but pasted as Key ID | Copy from correct field |
| Extra spaces before/after keys | Remove any extra whitespace |
| Mix of test and live keys | Use ALL test keys or ALL live keys |
| Old settings.py file | Make sure you're editing `config/settings.py` not `HomeRentalManagement/settings.py` |
| Server not restarted | Restart Django server after changes |

---

## Getting Live Keys (Later, Not Now!)

When you're ready for production:

1. Login to Razorpay dashboard
2. Go to Settings → API Keys
3. Find LIVE KEYS section
4. Complete business verification
5. Swap test keys with live keys in settings.py
6. Change DEBUG = False in settings
7. Enable HTTPS
8. Deploy to production

**For now, stick with test keys!** 🧪

---

**Time to completion**: 10 minutes ⏱️  
**Difficulty**: Easy 🟢  
**Cost**: Free 💰
