from django.contrib.auth import get_user_model
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

User = get_user_model()


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = PhoneNumberField(required=True)
    confirmation_code = serializers.IntegerField(read_only=True)


class ConfirmationCodeSerializer(PhoneNumberSerializer):
    confirmation_code = serializers.IntegerField(required=True)


class UserSerializer(serializers.ModelSerializer):
    invited_users = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('phone_number', 'invite_code',
                  'activated_code', 'invited_users')
        read_only_fields = ('phone_number', 'invite_code',)

    def validate(self, data):
        request = self.context.get('request')
        activated_code = request.data.get('activated_code')
        if not activated_code:
            return super().validate(data)
        if not User.objects.filter(invite_code=activated_code).exists():
            raise serializers.ValidationError(
                'User with this invite code does not exist.'
            )
        if request.user.activated_code and activated_code:
            raise serializers.ValidationError(
                'You have already activated an invite code.'
            )
        return super().validate(data)

    def get_invited_users(self, obj):
        invite_code = obj.invite_code
        return User.objects.filter(activated_code=invite_code).values_list(
            'phone_number'
        )
