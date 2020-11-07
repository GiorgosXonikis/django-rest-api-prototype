from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.helpers import generate_code

User = get_user_model()
SEX_CHOICES = (('Male', 'Male'), ('Female', 'Female'))


class UserProfile(models.Model):
    user = models.OneToOneField(
        verbose_name='user',
        to=User,
        on_delete=models.CASCADE,
        related_name='user_profile'
    )
    sex = models.CharField(max_length=6, choices=SEX_CHOICES, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    bio = models.CharField(max_length=500, blank=True)
    city = models.CharField(max_length=30, blank=True)
    phone = models.CharField(null=True, blank=True, max_length=30)
    avatar = models.ImageField(null=True, blank=True)
    code = models.CharField(
        verbose_name='code',
        max_length=255,
        default=generate_code,
    )

    def generate_new_code(self):
        self.code = generate_code()
        self.save()
        return self.code

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """ Define signal so the USer Profile model will be automatically created when we create User instance """
    if created:
        print('Created')
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """ Define signal so the User Profile model will be updated when we update the User instances """
    instance.user_profile.save()


