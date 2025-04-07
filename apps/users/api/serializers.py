from dj_rest_auth.serializers import UserDetailsSerializer
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

try:
    from allauth.account import app_settings as allauth_settings
    from allauth.utils import (email_address_exists,
                               get_username_max_length)
    from allauth.account.adapter import get_adapter
    from allauth.account.utils import setup_user_email
    from allauth.socialaccount.helpers import complete_social_login
    from allauth.socialaccount.models import SocialAccount
    from allauth.socialaccount.providers.base import AuthProcess
except ImportError:
    raise ImportError("allauth needs to be added to INSTALLED_APPS.")

from rest_framework import serializers


class RegisterOrGetUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(max_length=15, required=False)
    first_name = serializers.CharField(
        max_length=30,
        required=True
    )

    def validate_email(self, email):
        if email:
            email = get_adapter().clean_email(email)
        return email

    def validate_phone(self, phone):
        # Add any phone validation logic here if needed
        return phone

    def validate(self, data):
        # Ensure at least one of email or phone is provided
        if not data.get('email') and not data.get('phone'):
            raise serializers.ValidationError(
                _("Either email or phone number must be provided.")
            )
        return data

    def get_cleaned_data(self):
        return {
            'email': self.validated_data.get('email', ''),
            'phone': self.validated_data.get('phone', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'password1': str(self.validated_data.get('email', '')) + str(self.validated_data.get('phone', ''))

        }

    def save(self, request):
        user = None
        created = False

        email = self.validated_data.get('email')
        phone = self.validated_data.get('phone')
        first_name = self.validated_data.get('first_name')

        # Try to find an existing user by email or phone
        if email:
            try:
                user = get_user_model().objects.get(email=email)

            except get_user_model().DoesNotExist:
                pass

        if not user and phone:
            try:
                user = get_user_model().objects.get(phone=phone)

            except get_user_model().DoesNotExist:
                pass

        if user:
            # User exists and information matches
            # Update the other field if it was provided but is different
            if email and phone and user.email != email:
                user.email = email
                user.save(update_fields=['email'])
            elif email and phone and user.phone != phone:
                user.phone = phone
                user.save(update_fields=['phone'])

            return user  # False indicates user was not created

        # No user found, create a new one
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()

        # Set the fields directly
        if email:
            user.email = email
        if phone:
            user.phone = phone
        user.first_name = first_name

        # Set an unusable password
        user.set_unusable_password()

        # Save the user
        user.save()

        # self.custom_signup(request, user)
        if email:
            setup_user_email(request, user, [])
        return user  # True indicates user was created


class UserDetailsSerializer(UserDetailsSerializer):
    class Meta:
        model = get_user_model()
        fields = ('pk', "phone", "email", "first_name", "username")
        read_only_fields = ('email',)
