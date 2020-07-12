from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse


from ..forms import SignUpForm
from ..views import signup


class SignupTests(TestCase):
    def setUp(self):
        url = reverse("signup")
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        view = resolve("/signup/")
        self.assertEquals(view.func, signup)

    def test_csrf(self):
        self.assertContains(self.response, "csrfmiddlewaretoken")

    def test_contains_form(self):
        form = self.response.context.get("form")
        self.assertIsInstance(form, SignUpForm)

    def test_form_inputs(self):
        """
        The view must contain five inputs: csrf, username, email,
        password1, password2
        """
        self.assertContains(self.response, "<input", 5)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)


class SuccessfulSignUpTests(TestCase):
    def setUp(self):
        url = reverse("signup")
        data = {
            "username": "chino",
            "email": "nili@email.com",
            "password1": "qUYnQC2bRGbpVcu",
            "password2": "qUYnQC2bRGbpVcu",
        }

        self.response = self.client.post(url, data)
        self.signin_url = reverse("signin")

    def test_redirection(self):
        """
        A valid form submission should redirect the user to the sign in page
        """
        self.assertRedirects(self.response, self.signin_url)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())


class InvalidSignUpTests(TestCase):
    def setUp(self):
        url = reverse("signup")
        self.response = self.client.post(url, {})

    def test_signup_status_code(self):
        """
        An invalid form submission should return to the same page
        """
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get("form")
        self.assertTrue(form.errors)

    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())
