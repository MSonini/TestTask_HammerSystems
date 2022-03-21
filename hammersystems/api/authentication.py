from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import authentication, exceptions

from .serializers import ConfirmationCodeSerializer

User = get_user_model()


class UserSmsAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        serializer = ConfirmationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data.get('phone_number')
        confirmation_code = serializer.validated_data.get('confirmation_code')

        try:
            user = User.objects.get(
                phone_number=phone_number,
                confirmation_code=confirmation_code,
            )
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed(
                'Incorrect phone number or confirmation code.'
            )
        return (user, None)
