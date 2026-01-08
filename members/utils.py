# members/utils.py
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings


def send_verification_email(user, request):
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    verify_url = request.build_absolute_uri(
        reverse('verify_email', kwargs={'uidb64': uid, 'token': token})
    )
    subject = 'Verify your PSN Rivers Membership Email'
    text_message = f"""
Hello {user.first_name or user.email},

Thank you for registering at PSN Rivers.

Please verify your email by clicking the link below:

{verify_url}

If you did not register, please ignore this email.

PSN Rivers State Branch
"""
    html_message = render_to_string(
        'members/verify_email.html',
        {'user': user, 'verification_url': verify_url}
    )

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    email.attach_alternative(html_message, "text/html")
    email.send()


def send_clearance_email(user, subject, message, html_template=None, context=None):
    try:
        if html_template and context:
            html_message = render_to_string(html_template, context)
        else:
            html_message = None

        email = EmailMultiAlternatives(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        if html_message:
            email.attach_alternative(html_message, "text/html")
        email.send()
    except Exception as e:
        print(f"Clearance email send failed for {user.email}: {e}")
