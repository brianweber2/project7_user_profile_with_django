from django.test import TestCase
from django.test.client import RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.contrib.auth.forms import AuthenticationForm

from accounts.models import User, UserProfile, create_user_profile
from accounts.forms import * # import all forms

user_create_form_data = {
    'first_name': 'Test',
    'last_name': 'User',
    'email': 'testing@gmail.com',
    'verify_email': 'testing@gmail.com',
    'password1': 'Testing17!',
    'password2': 'Testing17!'
}

user_create_form_data_incorrect = {
    'first_name': 'Test',
    'last_name': 'User',
    'email': 'testing_gmail.com',
    'verify_email': 'testing@gmail.com',
    'password1': 'test!',
    'password2': 'test!'
}


class TestDataMixin():

    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.user1 = User.objects.create_user(
            first_name='Test',
            last_name='Client',
            email='testclient@example.com',
            password='password'
        )


################################
########## View Tests ##########
################################
class UserViewTests(TestDataMixin, TestCase):

    def test_profile_view(self):
        response = self.client.get(reverse('accounts:sign_in'))
        self.assertEqual(response.status_code, 200)

        self.client.login(email='testclient@example.com', password='password')

        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)

    def  test_edit_profile_view(self):
        response = self.client.get(reverse('accounts:sign_in'))
        self.assertEqual(response.status_code, 200)

        self.client.login(email='testclient@example.com', password='password')

        response = self.client.get(reverse('accounts:edit_profile'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('accounts:edit_profile'),
            {
                'first_name': 'Brian',
                'last_name': 'Weber',
                'email': 'testclient@example.com',
                'verify_email': 'testclient@example.com',
                'dob': '1988-06-19',
                'bio': 'This is my bio.',
                'location': 'San Diego, CA',
                'country': 'US',
                'fav_animal': 'Dog',
                'hobby': 'Surfing'
            }
        )
        self.assertEqual(response.status_code, 302)

    def test_change_password_view(self):
        response = self.client.get(reverse('accounts:sign_in'))
        self.assertEqual(response.status_code, 200)

        self.client.login(email='testclient@example.com', password='password')

        response = self.client.get(reverse('accounts:change_password'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('accounts:change_password'),
            {
                'old_password': 'password',
                'new_password1': 'Abu$edSurfer17!',
                'new_password2': 'Abu$edSurfer17!'
            }
        )
        self.assertEqual(response.status_code, 302)

    def test_sign_in_view(self):
        response = self.client.get(reverse('accounts:sign_in'))
        self.assertTemplateUsed(response, 'accounts/sign_in.html')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Sign In' in str(response.content))

        response = self.client.post(reverse('accounts:sign_in'),
            {'email': 'testclient@example.com', 'password': 'password'})
        self.client.login(email='testclient@example.com', password='password')
        self.assertEqual(response.status_code, 302)

    def test_sign_up_view(self):
        response = self.client.get(reverse('accounts:sign_up'))
        self.assertTemplateUsed(response, 'accounts/sign_up.html')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Sign Up' in str(response.content))

        response = self.client.post(reverse('accounts:sign_up'),
            {
                'first_name': 'Brian',
                'last_name': 'Weber',
                'email': 'brianweber2@gmail.com',
                'verify_email': 'brianweber2@gmail.com',
                'password1': 'surfing17',
                'password2': 'surfing17'
        })
        self.client.login(email='brianweber2@gmail.com', password='surfing17')
        self.assertEqual(response.status_code, 302)

    def test_sign_out_view(self):
        response = self.client.get(reverse('accounts:sign_in'))
        self.assertTemplateUsed(response, 'accounts/sign_in.html')
        self.assertEqual(response.status_code, 200)

        self.client.login(email='testclient@example.com', password='password')

        response = self.client.get(reverse('accounts:sign_out'))
        self.assertEqual(response.status_code, 302)


#################################
########## Model Tests ##########
#################################
class UserModelTests(TestDataMixin, TestCase):

    def test_user_creation_no_email(self):
        with self.assertRaises(ValueError):
            user = User.objects.create_user(
            first_name='Test',
            last_name='Client',
            email='',
            password='password'
            )

    def test_user_creation_no_first_name(self):
        with self.assertRaises(ValueError):
            user = User.objects.create_user(
                first_name='',
                last_name='Client',
                email='test@gmail.com',
                password='password'
            )

    def test_user_creation_no_last_name(self):
        with self.assertRaises(ValueError):
            user = User.objects.create_user(
                first_name='Test',
                last_name='',
                email='test@gmail.com',
                password='password'
            )

    def test_user_username(self):
        user = User.objects.create_user(
            first_name='Test',
            last_name='Client',
            email='test@gmail.com',
            password='password'
        )
        username = user.username
        self.assertEqual(username, 'test')

    def test_superuser_creation(self):
        user = User.objects.create_superuser(
            first_name='Test',
            last_name='Client',
            email='test@gmail.com',
            password='password'
        )
        self.assertEqual(user.is_staff, True)


################################
########## Form Tests ##########
################################
class UserSignInFormTests(TestDataMixin, TestCase):

    def test_user_login(self):
        data = {'username': 'testclient@example.com', 'password': 'password'}
        form = AuthenticationForm(data=data)
        self.assertTrue(form.is_valid())


class UserCreateFormTests(TestCase):

    # Valid form data
    def test_UserCreateForm_valid(self):
        form = UserCreateForm(data=user_create_form_data)
        self.assertTrue(form.is_valid())

    # Invalid form data
    def test_UserCreateForm_invalid(self):
        form = UserCreateForm(data=user_create_form_data_incorrect)
        self.assertFalse(form.is_valid())


class UserUpdateFormTests(TestCase):

    # Valid form data
    def test_UserUpdateForm_valid(self):
        form = UserUpdateForm(data={
            'first_name': 'Brian',
            'last_name': 'Weba',
            'email': 'brianweber2@gmail.com',
            'verify_email': 'brianweber2@gmail.com'
        })
        self.assertTrue(form.is_valid())

    # Invalid form data
    def test_UserUpdateForm_invalid(self):
        form = UserUpdateForm(data={
            'first_name': 'Brian',
            'last_name': 'Weba',
            'email': 'brianweber2@gmail.com',
            'verify_email': 'brianweber@gmail.com'
        })
        self.assertFalse(form.is_valid())


class ValidatingPasswordChangeFormTests(TestDataMixin, TestCase):

    def setUp(self):
        # Create a RequestFactory accessible by the entire class
        self.factory = RequestFactory()
        self.user = User.objects.get(email='testclient@example.com')

    # Valid form data
    def test_valid_form_data(self):
        request = self.factory.get('/accounts/profile/change_password/')
        request.user = self.user

        form = ValidatingPasswordChangeForm(
            user=request.user,
            data={
                'old_password': 'password',
                'new_password1': 'Abu$edSurfer17!',
                'new_password2': 'Abu$edSurfer17!'},
            request=request)
        self.assertTrue(form.is_valid())

    # Check if new password equals old password
    def test_new_password_equal_to_old_password(self):
        request = self.factory.get('/accounts/profile/change_password/')
        request.user = self.user

        form = ValidatingPasswordChangeForm(
            user=request.user,
            data={
                'old_password': 'password',
                'new_password1': 'password',
                'new_password2': 'password'},
            request=request)
        self.assertFalse(form.is_valid())

    # Check if old password was entered incorrectly
    def test_old_password_incorrect(self):
        request = self.factory.get('/accounts/profile/change_password/')
        request.user = self.user

        form = ValidatingPasswordChangeForm(
            user=request.user,
            data={
                'old_password': 'password1',
                'new_password1': 'password',
                'new_password2': 'password'},
            request=request)
        self.assertFalse(form.is_valid())

    # Check if new password has uppercase letters
    def test_new_password_upper_lettters(self):
        request = self.factory.get('/accounts/profile/change_password/')
        request.user = self.user

        form = ValidatingPasswordChangeForm(
            user=request.user,
            data={
                'old_password': 'password',
                'new_password1': 'therearenouppercaseletters',
                'new_password2': 'therearenouppercaseletters'},
            request=request)
        self.assertFalse(form.is_valid())

    # Check if new password has lowercase letters
    def test_new_password_lower_lettters(self):
        request = self.factory.get('/accounts/profile/change_password/')
        request.user = self.user

        form = ValidatingPasswordChangeForm(
            user=request.user,
            data={
                'old_password': 'password',
                'new_password1': 'THEREARENOLOWERCASELETTERS',
                'new_password2': 'THEREARENOLOWERCASELETTERS'},
            request=request)
        self.assertFalse(form.is_valid())

    # Check minimum length of new password
    def test_new_password_length(self):
        response = self.client.post('/accounts/profile/change_password/',
            {
                'old_password': 'password',
                'new_password1': 'tooShort',
                'new_password2': 'tooShort'
            }
        )
        self.assertFormError(response, 'form', 'new_password1', 'The new password must be at least 14 characters long.')

    # Check if there is a number in the new_password
    def test_new_password_length(self):
        request = self.factory.get('/accounts/profile/change_password/')
        request.user = self.user

        form = ValidatingPasswordChangeForm(
            user=request.user,
            data={
                'old_password': 'password',
                'new_password1': 'ThisPasswordIsLongEnough',
                'new_password2': 'ThisPasswordIsLongEnough'},
            request=request)
        self.assertFalse(form.is_valid())

    # Check if the new password includes at least one of @, #, or $
    def test_new_password_length(self):
        request = self.factory.get('/accounts/profile/change_password/')
        request.user = self.user

        form = ValidatingPasswordChangeForm(
            user=request.user,
            data={
                'old_password': 'password',
                'new_password1': 'ThisPasswordIsLongEnough1',
                'new_password2': 'ThisPasswordIsLongEnough1'},
            request=request)
        self.assertFalse(form.is_valid())

    # Check if the new password contains the username or parts of the user’s
    # full name, such as his first name
    def test_new_password_length(self):
        request = self.factory.get('/accounts/profile/change_password/')
        request.user = self.user

        form = ValidatingPasswordChangeForm(
            user=request.user,
            data={
                'old_password': 'password',
                'new_password1': 'Abu$edSurfer17!Test',
                'new_password2': 'Abu$edSurfer17!Test'},
            request=request)
        self.assertFalse(form.is_valid())
