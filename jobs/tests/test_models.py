from django.contrib.auth.models import User
from django.test import TestCase

from ..models import Job


class TestJob(TestCase):
    @classmethod
    def setUpTestData(cls):
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

    def test_creation(self):
        job = Job.objects.get(pk=1)
        self.assertIsNotNone(job)

    def test_str(self):
        job = Job.objects.get(pk=1)
        self.assertEquals(str(job), "Python developer at Django")

    def test_expires(self):
        """
        Test that the expires field is set as follows:
        
        expires = created + datetime.timedelta(days=JOB_DURATION_DAYS)
        """
        job = Job.objects.get(pk=1)
        self.assertIsNotNone(job.expires)
