# members/utils.py
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings

def send_verification_email(user, request):
    """
    Sends a verification email to the user with a unique link.
    The link includes the user's UID and token.
    """
    # Generate token and UID
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    # Build full verification URL
    verify_url = request.build_absolute_uri(
        reverse('verify_email', kwargs={'uidb64': uid, 'token': token})
    )

    # Email subject
    subject = 'Verify your PSN Rivers Membership Email'

    # Email body (plain text)
    message = f"""
Hello {user.first_name},

Thank you for registering at PSN Rivers.

Please verify your email by clicking the link below:

{verify_url}

If you did not register, please ignore this email.

Thank you!
"""

    # ✅ Actually send the email
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False
        )
    except Exception as e:
        print("Email send failed:", e)
