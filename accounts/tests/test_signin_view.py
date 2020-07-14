from django.test import TestCase
from django.urls import resolve, reverse


from ..forms import SignInForm
from ..views import signin


class SigninTests(TestCase):
    def setUp(self):
        url = reverse("signin")
        self.response = self.client.get(url)

    def test_signin_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_signin_url_resolves_sigin_view(self):
        view = resolve("/signin/")
        self.assertEquals(view.func, signin)

    def test_csrf(self):
        self.assertContains(self.response, "csrfmiddlewaretoken")

    def test_contains_form(self):
        form = self.response.context.get("form")
        self.assertIsInstance(form, SignInForm)

    def test_form_inputs(self):
        """
        The view must contain four inputs: csrf, next, email, password
        """
        self.assertContains(self.response, "<input", 4)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 1)


class BaseTest(TestCase):
    def setUp(self):
        self.signin_url = reverse("signin")
        self.signup_url = reverse("signup")
        self.home_url = reverse("list_jobs")
        self.user = {
            "email": "chino@email.com",
            "password": "qUYnQC2bRGbpVcu",
        }

        # sign up user
        self.client.post(
            self.signup_url,
            {
                "username": "chino",
                "email": "chino@email.com",
                "password1": "qUYnQC2bRGbpVcu",
                "password2": "qUYnQC2bRGbpVcu",
            },
        )

        # sign in user
        self.response = self.client.post(self.signin_url, self.user)


class SuccessfulSigninTests(BaseTest):
    def test_redirection(self):
        """
        A valid form submission should redirect the user to the sign in page
        """
        self.assertEquals(self.response.status_code, 302)

    def test_user_authentication(self):
        """
        Create a new request to an arbitrary page.
        The resulting response should now have a `user` to its context,
        after a successful sign in.
        """
        response = self.client.get(self.home_url)
        user = response.context.get("user")
        self.assertTrue(user.is_authenticated)


class InvalidSigninTest(BaseTest):
    def test_cant_signin_no_email(self):
        """
        An invalid form submission should return to the same page
        """
        response = self.client.post(self.signin_url, {"password": "qUYnQC2bRGbpVcu"})
        self.assertEquals(response.status_code, 200)

    def test_cant_signin_no_password(self):
        """
        An invalid form submission should return to the same page
        """
        response = self.client.post(self.signin_url, {"email": "chino@email.com"})
        self.assertEquals(response.status_code, 200)

    def test_cant_signin_incorrect_password(self):
        """
        An invalid form submission should return to the same page
        """
        response = self.client.post(
            self.signin_url, {"email": "chino@email.com", "password": "my_password"}
        )
        self.assertEquals(response.status_code, 200)

