from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail import send_mail

email_messages = {
    'after_registration': {'subject': 'Welcome! Your account has been created', 'message': f'Hi,\nThank you for registering with us! Your account has been successfully created. We are happy to have you on board!'},

    'after_contact_us': {'subject': 'We’ve received your request', 'message': f'''Hello,
    Thank you for reaching out to us. We’ve received your request and it will be reviewed shortly.
    If you have any further questions or need assistance in the meantime, feel free to contact us at {settings.EMAIL_HOST_USER}.
    Best regards,
    [Your Company Name]'''},

    'after_change_password': {'subject': 'Your Password Has Been Changed', 'message': f'''Hello,
    We wanted to inform you that your password has been successfully changed.
    If you did not request this change, please contact us immediately at {settings.EMAIL_HOST_USER}.
    Best regards,
    [Your Company Name]'''}
}

def send_contact_email_reply(subject, message, email):
    email = EmailMessage(
        subject = subject,
        body = message,
        from_email = settings.DEFAULT_FROM_EMAIL,
        to = [settings.EMAIL_HOST_USER],
        reply_to = [email]
    )
    email.send(fail_silently=False)

def send_email_for_person(subject, message, email):
    send_mail(
        subject = subject,
        message = message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email]
    )