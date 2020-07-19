import tempfile

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from PIL import Image

from ..forms import NewJobForm
from ..models import Job
from ..views import post_job


class TestPostJob(TestCase):
    def setUp(self):
        self.url = reverse("post_job")
        self.user = User.objects.create_user("Chino", "chino@email.com", "django")

    def test_unauthenticated_access(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)

    def test_get(self):
        # the password should be plain text
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

    def test_contains_form(self):
        self.client.login(username=self.user.username, password="django")
        response = self.client.get(self.url)
        form = response.context.get("form")
        self.assertIsInstance(form, NewJobForm)


class TestListJobsView(TestCase):
    def setUp(self):
        self.url = reverse("list_jobs")
        User.objects.create(username="Chino", password="django")
        Job.objects.create(
            title="Python developer",
            link_to_apply="https://docs.djangoproject.com",
            job_type="Full-time",
            location="",
            remote=True,
            description="The best job ever.",
            company="Django",
            company_logo="logo.png",
            posted_by=User.objects.get(pk=1),
        )

        Job.objects.create(
            title="Django developer",
            link_to_apply="https://www.squarespace.com/",
            job_type="Part-time",
            location="",
            remote=True,
            description="The best job ever.",
            company="Squarespace",
            company_logo="logo.png",
            posted_by=User.objects.get(pk=1),
        )

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_has_job_type(self):
        """
        Assert that job_type is in context when filtering by job type.
        """
        response = self.client.get(self.url + "?job_type=Full-time")
        job_type = response.context.get("job_type")
        self.assertIsNotNone(job_type)
