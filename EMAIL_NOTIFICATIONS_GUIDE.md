# Email Notifications System - RentEase

## Overview
The email notification system automatically sends emails to users when they receive new messages in conversations. This keeps users engaged and ensures they don't miss important communications.

## Features Implemented

### 1. New Message Notifications
- **Trigger**: When a user sends a message in a conversation
- **Recipient**: The other party in the conversation (owner or tenant)
- **Content**: 
  - Sender's name
  - Message preview (first 100 characters)
  - Direct link to the conversation
  - Branded email template with RentEase logo

### 2. Inquiry Notifications
- **Trigger**: When a tenant sends an inquiry about a property
- **Recipient**: Property owner
- **Content**:
  - Tenant's name
  - Full inquiry message
  - Property title
  - Direct link to view the property

## Email Configuration

### Development Mode (Current Setup)
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```
- Emails are printed to the console/terminal
- No actual emails are sent
- Perfect for testing and development

### Production Mode (Gmail Example)

To send real emails in production, update `config/settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'  # Use App Password
DEFAULT_FROM_EMAIL = 'RentEase <your-email@gmail.com>'
```

### Setting Up Gmail App Password

1. Go to your Google Account settings
2. Navigate to Security → 2-Step Verification
3. Scroll down to "App passwords"
4. Generate a new app password for "Mail"
5. Use this 16-character password in `EMAIL_HOST_PASSWORD`

### Other Email Providers

**SendGrid:**
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = 'your-sendgrid-api-key'
```

**Mailgun:**
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mailgun.org'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'postmaster@your-domain.mailgun.org'
EMAIL_HOST_PASSWORD = 'your-mailgun-password'
```

## Email Template Design

The email templates feature:
- **Responsive design** - Works on all devices
- **Branded header** - RentEase logo with gold and cream colors
- **Clear call-to-action** - Prominent button to view messages
- **Professional styling** - Matches the website's black and cream theme
- **HTML + Plain text** - Fallback for email clients that don't support HTML

## Testing Email Notifications

### 1. Console Backend (Development)
```bash
# Start the Django development server
python manage.py runserver

# Send a message through the app
# Check the console/terminal for the email output
```

### 2. Test with Real Email
```python
# In Django shell
python manage.py shell

from django.core.mail import send_mail
send_mail(
    'Test Email',
    'This is a test message.',
    'noreply@rentease.com',
    ['your-email@example.com'],
    fail_silently=False,
)
```

## File Structure

```
core/
├── email_utils.py              # Email utility functions
└── views.py                    # Updated with email notifications

config/
└── settings.py                 # Email configuration
```

## Functions Available

### `send_new_message_notification()`
```python
from core.email_utils import send_new_message_notification

send_new_message_notification(
    recipient=user_object,
    sender=sender_object,
    message_preview="Hello, I'm interested...",
    conversation_url="https://yoursite.com/conversations/1/"
)
```

### `send_inquiry_notification()`
```python
from core.email_utils import send_inquiry_notification

send_inquiry_notification(
    property_owner=owner_object,
    tenant=tenant_object,
    property_title="2 BHK Apartment",
    inquiry_message="Is this property still available?",
    property_url="https://yoursite.com/property/1/"
)
```

## Customization

### Change Email Template Colors
Edit `core/email_utils.py` and modify the CSS in the HTML templates:
- Background colors
- Button styles
- Font sizes
- Logo styling

### Add More Notification Types
Create new functions in `core/email_utils.py`:
- Application status updates
- Payment confirmations
- Plan expiry reminders
- Property approval notifications

### Disable Notifications
To temporarily disable email notifications, comment out the email sending code in `core/views.py` or set:
```python
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
```

## Best Practices

1. **Don't Block Requests**: Email sending is wrapped in try-except to prevent failures from blocking user actions
2. **Use App Passwords**: Never use your actual Gmail password
3. **Rate Limiting**: Consider implementing rate limiting for production
4. **Unsubscribe Option**: Add unsubscribe links for compliance
5. **Email Verification**: Verify user emails before sending notifications
6. **Queue System**: For high-volume apps, use Celery for async email sending

## Troubleshooting

### Emails Not Sending
1. Check `EMAIL_BACKEND` setting
2. Verify SMTP credentials
3. Check firewall/port settings
4. Look for errors in console/logs

### Gmail Blocking Emails
1. Enable "Less secure app access" (not recommended)
2. Use App Passwords (recommended)
3. Check Google's security alerts

### Emails Going to Spam
1. Set up SPF records
2. Configure DKIM
3. Use a verified domain
4. Avoid spam trigger words

## Future Enhancements

- [ ] Email preferences (let users choose notification types)
- [ ] Digest emails (daily/weekly summaries)
- [ ] SMS notifications integration
- [ ] Push notifications for mobile
- [ ] Email templates in database (editable via admin)
- [ ] A/B testing for email content
- [ ] Email analytics (open rates, click rates)

## Security Considerations

- Store email credentials in environment variables
- Use encrypted connections (TLS/SSL)
- Implement rate limiting
- Validate email addresses
- Add CAPTCHA for public forms
- Monitor for abuse

## Support

For issues or questions:
1. Check Django documentation: https://docs.djangoproject.com/en/stable/topics/email/
2. Review email provider documentation
3. Check application logs for errors

---

**Status**: ✅ Implemented and Ready for Testing
**Last Updated**: March 13, 2026
