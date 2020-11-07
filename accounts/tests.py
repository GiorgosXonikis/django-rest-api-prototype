from unittest import TestCase

from django.contrib.auth import get_user_model

from accounts.models import UserProfile


class UserProfileTests(TestCase):

    @classmethod
    def setUp(self):
        User = get_user_model()

        # Create a test user
        self.test_user = User.objects.create_user(
            username='test_user',
            email='test_user@email.com',
            password='test1234'
        )
        self.test_user.save()

        # Update user profile
        self.id = User.objects.get(username='test_user').id
        self.user_profile = UserProfile.objects.get(id=self.id)
        self.user_profile.age = 35
        self.user_profile.bio = 'Lorem Ipsum'
        self.user_profile.city = 'Zurich'

    def test_create_user(self):
        self.assertEqual(self.test_user.username, 'test_user')
        self.assertEqual(self.test_user.email, 'test_user@email.com')
        self.assertTrue(self.test_user.check_password('test1234'))

    def test_update_user_profile(self):
        self.assertEqual(self.user_profile.age, 35)
        self.assertEqual(self.user_profile.bio, 'Lorem Ipsum')
        self.assertEqual(self.user_profile.city, 'Zurich')

    def tearDown(self):
        self.test_user.delete()
