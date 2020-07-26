from django.test import TestCase
from django.urls import reverse

from .factories import JobFactory


class TestJob(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.job = JobFactory()

    def test_creation(self):
        self.assertIsNotNone(TestJob.job)

    def test_str(self):
        job = TestJob.job
        self.assertEquals(str(job), f"{job.title} at {job.company}")

    def test_expires(self):
        """
        Test that the expires field is set as follows:

        expires = created + datetime.timedelta(days=JOB_DURATION_DAYS)
        """
        job = TestJob.job
        self.assertIsNotNone(job.expires)

    def test_absolute_url(self):
        job = TestJob.job
        self.assertEquals(
            job.get_absolute_url(), reverse("job_detail", kwargs={"pk": 1})
        )
