from django.core.mail import send_mail
from django.conf import settings
from rest_framework.authentication import get_authorization_header
from rest_framework import exceptions
from django.conf import settings
import jwt


def send_custom_mail(subject, message, recipients):
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipients)


def check_token(request):

    auth_header = get_authorization_header(request)

    auth_data = auth_header.decode('utf-8')

    auth_token = auth_data.split(" ")

    if len(auth_token) != 2:
        raise exceptions.AuthenticationFailed('Token not Valid')

    token = auth_token[1]
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY2, algorithms='HS256')

        return payload

    except jwt.ExpiredSignatureError as ex:
        raise exceptions.AuthenticationFailed(
            'Token expired, login again')

    except jwt.DecodeError as ex:
        raise exceptions.AuthenticationFailed(
            'Token is invalid')


def recover_email(email, uncripted_code):
    send_custom_mail(
        subject="recover password",
        message=f"This the your code to recover the Password {uncripted_code},I'll be valid for one hour.",
        recipients=[email],
    )


def get_objet_summary(Object, start_date, end_date):

    return Object.objects.filter(created_at__gte=start_date,
                                 created_at__lte=end_date,
                                 )
