import tempfile

from django.test import TestCase
from django.urls import resolve, reverse

from PIL import Image

from accounts.tests.factories import UserFactory

from .factories import JobFactory
from ..forms import NewJobForm
from ..models import Job
from ..views import post_job


class TestPostJob(TestCase):
    def setUp(self):
        self.url = reverse("post_job")
        self.user = UserFactory()

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
        UserFactory()

        JobFactory(job_type="Full-time")
        JobFactory(job_type="Part-time")

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


class TestJobDeleteView(TestCase):
    def setUp(self):
        self.url = reverse("job_delete", kwargs={"pk": 1})
        self.user1 = UserFactory()
        self.user2 = UserFactory()

        JobFactory(posted_by=self.user1)

    def test_unauthenticated_access(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)

    def test_post(self):
        # the password should be plain text
        self.client.login(username=self.user1.username, password="django")
        response = self.client.post(self.url)
        self.assertEquals(Job.objects.count(), 0)
        self.assertEquals(response.status_code, 302)

    def test_post_other_user(self):
        """
        A job should only be deleted by the user that created it.

        Expecting: 403 Forbidden
        """
        self.client.login(username=self.user2.username, password="django")
        response = self.client.post(self.url)
        self.assertEquals(response.status_code, 403)
        self.assertTemplateUsed(response, "403.html")


class TestJobDetailView(TestCase):
    def setUp(self):
        self.url = reverse("job_detail", kwargs={"pk": 1})
        UserFactory()
        JobFactory()

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)


class TestJobUpdateView(TestCase):
    def setUp(self):
        self.url = reverse("job_update", kwargs={"pk": 1})
        self.user1 = UserFactory()
        self.user2 = UserFactory()

        JobFactory(posted_by=self.user1)

    def test_unauthenticated_access(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 302)

    def test_get(self):
        # the password should be plain text
        self.client.login(username=self.user1.username, password="django")
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 200)

    def test_unauthorized_access(self):
        """
        A job should only be edited by the user that created it.

        Expecting: 403 Forbidden
        """
        self.client.login(username=self.user2.username, password="django")
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, 403)
        self.assertTemplateUsed(response, "403.html")

