from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueValidator
from django.template import loader


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
        context = {'code': code}
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
    email = serializers.EmailField()
    validation_code = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        user = get_object_or_404(User, email=email)
        if attrs.get('validation_code') != user.user_profile.code or user.is_active:
            raise serializers.ValidationError({
                'code': 'Invalid code or user is already validated!',
            })
        return attrs

    def save(self, validated_data):
        user = get_object_or_404(User, email=validated_data['email'])
        user.is_active = True
        user.save()
        return user
