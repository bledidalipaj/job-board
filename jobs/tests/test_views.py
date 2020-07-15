import tempfile

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from PIL import Image

from ..forms import NewJobForm
from ..views import post_job


class TestPostJob(TestCase):
    def setUp(self):
        self.url = reverse("post_job")
        self.user = User.objects.create_user("Chino", "chino@email.com", "django")

    def test_unauthenticated_access(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)

    def test_get(self):
        self.client.login(username=self.user.username, password="django")
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_post(self):
        self.client.login(username=self.user.username, password="django")

        # creating image file
        image = Image.new("RGB", (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix=".png")
        image.save(tmp_file)
        tmp_file.seek(0)

        data = {
            "title": "Python developer",
            "link_to_apply": "https://docs.djangoproject.com",
            "job_type": "Full-time",
            "location": "",
            "remote": True,
            "description": "The best job ever.",
            "company": "Django",
            "company_website": "https://docs.djangoproject.com",
            "company_logo": tmp_file,
        }

        response = self.client.post(self.url, data)

        self.assertEquals(response.status_code, 302)

    def test_invalid_post(self):
        self.client.login(username=self.user.username, password="django")
        response = self.client.post(self.url, {})
        self.assertEquals(response.status_code, 200)

    def test_post_job_url_resolves_post_job_view(self):
        view = resolve("/post_job/")
        self.assertEquals(view.func, post_job)

    # def test_csrf(self):
    #     self.assertContains(self.response, "csrfmiddlewaretoken")

    def test_contains_form(self):
        self.client.login(username=self.user.username, password="django")
        response = self.client.get(self.url)
        form = response.context.get("form")
        self.assertIsInstance(form, NewJobForm)

    # def test_form_inputs(self):
    #     """
    #     The view must contain nine inputs:
    #         - csrf
    #         - title
    #         - link_to_apply
    #         - job_type
    #         - location
    #         - remote
    #         - descritpion
    #         - company
    #         - company_logo
    #     """
    #     self.client.login(username=self.user.username, password=self.user.password)
    #     response = self.client.get(reverse("post_job"))
    #     self.assertContains(response, "<input", 9)
