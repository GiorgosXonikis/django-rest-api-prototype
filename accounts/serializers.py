from dj_rest_auth.serializers import PasswordResetSerializer
from rest_framework import serializers
from accounts.models import UserProfile
from django.contrib.auth import get_user_model
from django.template import loader
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from rest_framework.generics import get_object_or_404

from config import settings

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    """
    User Profile Serializer
    """
    class Meta:
        model = UserProfile
        fields = ('sex', 'age', 'bio', 'location', 'languages', 'phone', 'avatar')


class CustomUserDetailsSerializer(serializers.ModelSerializer):
    """
    Serializer to return the User Profile on Login
    """
    user_profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ('pk', 'username', 'email', 'first_name', 'last_name', 'user_profile')
        read_only_fields = ('email', )


class CustomPasswordResetSerializer(PasswordResetSerializer):
    """
    Override Serializer's email options thr reset e-mail.
    """

    def get_email_options(self):
        """Override this method to change default e-mail options"""
        email = self.validated_data['email']
        user = get_object_or_404(User, email=email)

        template = loader.get_template('reset_password_email.html')
        subject = "Active Citizen -  Reset Password"
        context = {
            'email': email,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'user': user,
            'token': default_token_generator.make_token(user),
        }
        template = template.render(context)
        message = EmailMessage(subject, template, to=[email])
        message.content_subtype = 'html'

        message.send()

    def save(self):
        self.get_email_options()



