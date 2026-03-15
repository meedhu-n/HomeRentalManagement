"""
Email utility functions for RentEase
"""
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def send_new_message_notification(recipient, sender, message_preview, conversation_url):
    """
    Send email notification when a user receives a new message
    
    Args:
        recipient: User object who receives the message
        sender: User object who sent the message
        message_preview: Preview text of the message (first 100 chars)
        conversation_url: Full URL to the conversation
    """
    subject = f'New message from {sender.username}'
    
    # HTML email content
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: 'Poppins', Arial, sans-serif;
                background-color: #f5f5f5;
                margin: 0;
                padding: 0;
            }}
            .email-container {{
                max-width: 600px;
                margin: 40px auto;
                background: #ffffff;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            }}
            .email-header {{
                background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
                padding: 30px;
                text-align: center;
            }}
            .logo {{
                color: #f5f0e1;
                font-size: 32px;
                font-weight: 800;
                letter-spacing: 1px;
            }}
            .logo-rent {{
                color: #f5a623;
                font-style: italic;
            }}
            .logo-ease {{
                color: #f5f0e1;
                font-style: italic;
            }}
            .email-body {{
                padding: 40px 30px;
            }}
            .greeting {{
                font-size: 20px;
                font-weight: 600;
                color: #1a1a1a;
                margin-bottom: 20px;
            }}
            .message-box {{
                background: #f5f0e1;
                border-left: 4px solid #f5a623;
                padding: 20px;
                margin: 20px 0;
                border-radius: 8px;
            }}
            .sender-name {{
                font-weight: 700;
                color: #f5a623;
                margin-bottom: 10px;
            }}
            .message-preview {{
                color: #333;
                line-height: 1.6;
                font-style: italic;
            }}
            .cta-button {{
                display: inline-block;
                background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
                color: #f5f0e1;
                padding: 15px 40px;
                text-decoration: none;
                border-radius: 50px;
                font-weight: 700;
                margin: 20px 0;
                text-align: center;
            }}
            .email-footer {{
                background: #f5f5f5;
                padding: 20px;
                text-align: center;
                color: #666;
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="email-header">
                <div class="logo">
                    <span class="logo-rent">Rent</span><span class="logo-ease">Ease</span>
                </div>
            </div>
            <div class="email-body">
                <div class="greeting">Hi {recipient.username},</div>
                <p>You have a new message on RentEase!</p>
                
                <div class="message-box">
                    <div class="sender-name">From: {sender.username}</div>
                    <div class="message-preview">"{message_preview}..."</div>
                </div>
                
                <p>Click the button below to view and reply to this message:</p>
                
                <a href="{conversation_url}" class="cta-button">View Message</a>
                
                <p style="color: #666; font-size: 14px; margin-top: 30px;">
                    This is an automated notification. Please do not reply to this email.
                </p>
            </div>
            <div class="email-footer">
                <p>&copy; 2026 RentEase. All rights reserved.</p>
                <p>You're receiving this email because you have an account on RentEase.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Plain text version (fallback)
    plain_message = f"""
    Hi {recipient.username},
    
    You have a new message on RentEase!
    
    From: {sender.username}
    Message: "{message_preview}..."
    
    View and reply to this message: {conversation_url}
    
    ---
    This is an automated notification from RentEase.
    © 2026 RentEase. All rights reserved.
    """
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def send_inquiry_notification(property_owner, tenant, property_title, inquiry_message, property_url):
    """
    Send email notification when a property owner receives an inquiry
    
    Args:
        property_owner: User object (property owner)
        tenant: User object (tenant who sent inquiry)
        property_title: Title of the property
        inquiry_message: The inquiry message
        property_url: Full URL to the property
    """
    subject = f'New inquiry for your property: {property_title}'
    
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: 'Poppins', Arial, sans-serif;
                background-color: #f5f5f5;
                margin: 0;
                padding: 0;
            }}
            .email-container {{
                max-width: 600px;
                margin: 40px auto;
                background: #ffffff;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            }}
            .email-header {{
                background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
                padding: 30px;
                text-align: center;
            }}
            .logo {{
                color: #f5f0e1;
                font-size: 32px;
                font-weight: 800;
                letter-spacing: 1px;
            }}
            .logo-rent {{
                color: #f5a623;
                font-style: italic;
            }}
            .logo-ease {{
                color: #f5f0e1;
                font-style: italic;
            }}
            .email-body {{
                padding: 40px 30px;
            }}
            .greeting {{
                font-size: 20px;
                font-weight: 600;
                color: #1a1a1a;
                margin-bottom: 20px;
            }}
            .property-title {{
                font-size: 18px;
                font-weight: 700;
                color: #f5a623;
                margin: 20px 0;
            }}
            .inquiry-box {{
                background: #f5f0e1;
                border-left: 4px solid #f5a623;
                padding: 20px;
                margin: 20px 0;
                border-radius: 8px;
            }}
            .tenant-name {{
                font-weight: 700;
                color: #1a1a1a;
                margin-bottom: 10px;
            }}
            .inquiry-text {{
                color: #333;
                line-height: 1.6;
                font-style: italic;
            }}
            .cta-button {{
                display: inline-block;
                background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
                color: #f5f0e1;
                padding: 15px 40px;
                text-decoration: none;
                border-radius: 50px;
                font-weight: 700;
                margin: 20px 0;
                text-align: center;
            }}
            .email-footer {{
                background: #f5f5f5;
                padding: 20px;
                text-align: center;
                color: #666;
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="email-header">
                <div class="logo">
                    <span class="logo-rent">Rent</span><span class="logo-ease">Ease</span>
                </div>
            </div>
            <div class="email-body">
                <div class="greeting">Hi {property_owner.username},</div>
                <p>You have received a new inquiry for your property!</p>
                
                <div class="property-title">Property: {property_title}</div>
                
                <div class="inquiry-box">
                    <div class="tenant-name">From: {tenant.username}</div>
                    <div class="inquiry-text">"{inquiry_message}"</div>
                </div>
                
                <p>Click the button below to view your property and respond to the inquiry:</p>
                
                <a href="{property_url}" class="cta-button">View Property</a>
                
                <p style="color: #666; font-size: 14px; margin-top: 30px;">
                    This is an automated notification. Please do not reply to this email.
                </p>
            </div>
            <div class="email-footer">
                <p>&copy; 2026 RentEase. All rights reserved.</p>
                <p>You're receiving this email because you have an account on RentEase.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    plain_message = f"""
    Hi {property_owner.username},
    
    You have received a new inquiry for your property!
    
    Property: {property_title}
    From: {tenant.username}
    Message: "{inquiry_message}"
    
    View your property: {property_url}
    
    ---
    This is an automated notification from RentEase.
    © 2026 RentEase. All rights reserved.
    """
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[property_owner.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def send_property_rejection_notification(property_owner, property_title, rejection_reason, dashboard_url):
    """
    Send email notification when a property is rejected by admin
    
    Args:
        property_owner: User object (property owner)
        property_title: Title of the rejected property
        rejection_reason: Reason for rejection provided by admin
        dashboard_url: Full URL to the owner's dashboard
    """
    subject = f'Property Listing Rejected: {property_title}'
    
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: 'Poppins', Arial, sans-serif;
                background-color: #f5f5f5;
                margin: 0;
                padding: 0;
            }}
            .email-container {{
                max-width: 600px;
                margin: 40px auto;
                background: #ffffff;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            }}
            .email-header {{
                background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
                padding: 30px;
                text-align: center;
            }}
            .logo {{
                color: #ffffff;
                font-size: 32px;
                font-weight: 800;
                letter-spacing: 1px;
            }}
            .email-body {{
                padding: 40px 30px;
            }}
            .greeting {{
                font-size: 20px;
                font-weight: 600;
                color: #1a1a1a;
                margin-bottom: 20px;
            }}
            .property-title {{
                font-size: 18px;
                font-weight: 700;
                color: #dc3545;
                margin: 20px 0;
            }}
            .rejection-box {{
                background: #fff3cd;
                border-left: 4px solid #dc3545;
                padding: 20px;
                margin: 20px 0;
                border-radius: 8px;
            }}
            .rejection-label {{
                font-weight: 700;
                color: #dc3545;
                margin-bottom: 10px;
                text-transform: uppercase;
                font-size: 14px;
            }}
            .rejection-text {{
                color: #333;
                line-height: 1.6;
            }}
            .cta-button {{
                display: inline-block;
                background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%);
                color: #f5f0e1;
                padding: 15px 40px;
                text-decoration: none;
                border-radius: 50px;
                font-weight: 700;
                margin: 20px 0;
                text-align: center;
            }}
            .email-footer {{
                background: #f5f5f5;
                padding: 20px;
                text-align: center;
                color: #666;
                font-size: 12px;
            }}
            .info-box {{
                background: #e7f3ff;
                border-left: 4px solid #0066cc;
                padding: 15px;
                margin: 20px 0;
                border-radius: 8px;
                font-size: 14px;
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="email-header">
                <div class="logo">Property Listing Rejected</div>
            </div>
            <div class="email-body">
                <div class="greeting">Hi {property_owner.username},</div>
                <p>We regret to inform you that your property listing has been rejected by our admin team.</p>
                
                <div class="property-title">Property: {property_title}</div>
                
                <div class="rejection-box">
                    <div class="rejection-label">Reason for Rejection:</div>
                    <div class="rejection-text">{rejection_reason}</div>
                </div>
                
                <div class="info-box">
                    <strong>What's Next?</strong><br>
                    Please review the rejection reason and make necessary corrections. You can then submit a new listing that meets our guidelines.
                </div>
                
                <p>If you have any questions or need clarification, please contact our support team.</p>
                
                <a href="{dashboard_url}" class="cta-button">Go to Dashboard</a>
                
                <p style="color: #666; font-size: 14px; margin-top: 30px;">
                    This is an automated notification. Please do not reply to this email.
                </p>
            </div>
            <div class="email-footer">
                <p>&copy; 2026 RentEase. All rights reserved.</p>
                <p>You're receiving this email because you have an account on RentEase.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    plain_message = f"""
    Hi {property_owner.username},
    
    We regret to inform you that your property listing has been rejected.
    
    Property: {property_title}
    
    Reason for Rejection:
    {rejection_reason}
    
    What's Next?
    Please review the rejection reason and make necessary corrections. You can then submit a new listing that meets our guidelines.
    
    Go to your dashboard: {dashboard_url}
    
    If you have any questions, please contact our support team.
    
    ---
    This is an automated notification from RentEase.
    © 2026 RentEase. All rights reserved.
    """
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[property_owner.email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

