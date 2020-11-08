from rest_framework import serializers
from accounts.models import UserProfile
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('sex', 'age', 'bio', 'city', 'phone', 'avatar')


class CustomUserDetailsSerializer(serializers.ModelSerializer):
    """
    Serializer to return the User Detail on Login
    """
    user_profile = UserProfileSerializer()

    class Meta:
        model = UserModel
        fields = ('pk', 'username', 'email', 'first_name', 'last_name', 'user_profile')
        read_only_fields = ('email', )
