import string
from secrets import randbelow, choice

from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import PhoneNumberSerializer, UserSerializer
from .permissions import IsOwner, ReadOnly
from .authentication import UserSmsAuthentication

User = get_user_model()


@api_view(['POST'])
def get_confirmation_code(request):
    serializer = PhoneNumberSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    phone_number = serializer.validated_data.get('phone_number')

    alphabet = string.ascii_letters + string.digits
    invite_code = ''.join(choice(alphabet) for _ in range(6))
    confirmation_code = ''.join(str(randbelow(10)) for _ in range(4))

    defaults = {
        'invite_code': invite_code,
        'confirmation_code': confirmation_code,
    }
    user, created = User.objects.update_or_create(
        phone_number=phone_number, defaults=defaults)

    data = {
        'phone_number': str(phone_number),
        'confirmation_code': confirmation_code
    }

    return Response(data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwner | ReadOnly]
    authentication_classes = [UserSmsAuthentication]

    @action(
        methods=['patch', 'get'],
        permission_classes=[IsAuthenticated],
        detail=False,
        url_path='me',
        url_name='me'
    )
    def me(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(user)
        if self.request.method == 'PATCH':
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data)
