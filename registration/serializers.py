from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueValidator
from django.template import loader
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes


User = get_user_model()


class RegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label='Registration E-mail Address',
        validators=[UniqueValidator(queryset=User.objects.all(), message="Email already in use", )]
    )
    password = serializers.CharField()
    password_repeat = serializers.CharField()

    def validate_password(self, value):
        try:
            validate_password(value)
            return value
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_repeat'):
            raise serializers.ValidationError({
                'password_repeat': 'passwords do not match'
            })
        return attrs

    @staticmethod
    def send_registration_email(email, code):
        template = loader.get_template('registration_email.html')
        subject = "Your Active Citizen Registration"
        context = {
            'code_encoded': urlsafe_base64_encode(force_bytes(code)),
            'email_encoded': urlsafe_base64_encode(force_bytes(email))
        }
        template = template.render(context)
        message = EmailMessage(subject, template, to=[email])
        message.content_subtype = 'html'

        message.send()

    def save(self, validated_data):
        email = validated_data.get('email')
        new_user = User.objects.create_user(
            username=email,
            email=email,
            is_active=False,
        )
        self.send_registration_email(email, new_user.user_profile.code)
        new_user.set_password(validated_data.get('password'))
        new_user.save()
        return new_user


class RegistrationVerificationSerializer(serializers.Serializer):
    email = serializers.CharField()
    validation_code = serializers.CharField()

    def validate(self, attrs):
        _email = urlsafe_base64_decode(attrs.get('email')).decode()
        _validation_code = urlsafe_base64_decode(attrs.get('validation_code')).decode()
        user = get_object_or_404(User, email=_email)
        if _validation_code != user.user_profile.code:
            raise serializers.ValidationError({
                'code_error': 'Invalid validation code',
            })
        if user.is_active:
            raise serializers.ValidationError({
                'active_error': 'User is already active',
            })
        return attrs

    def save(self, validated_data):
        _email = urlsafe_base64_decode(validated_data['email']).decode()
        user = get_object_or_404(User, email=_email)
        user.is_active = True
        user.save()
        return user
