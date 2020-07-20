from django.contrib.auth.models import User
from django.db import models
from django.utils.safestring import mark_safe

from markdown import markdown


class Job(models.Model):
    FULL_TIME = "Full-time"
    PART_TIME = "Part-time"
    FREELANCE = "Freelance"
    CONTRACT = "Contract"

    JOB_TYPE_CHOICES = [
        (FULL_TIME, "Full-time"),
        (PART_TIME, "Part-time"),
        (FREELANCE, "Freelance"),
        (CONTRACT, "Contract"),
    ]

    title = models.CharField(max_length=255)
    link_to_apply = models.URLField(max_length=255)
    job_type = models.CharField(
        max_length=9, choices=JOB_TYPE_CHOICES, default=FULL_TIME
    )
    location = models.CharField(max_length=255, null=True, blank=True)
    remote = models.BooleanField()
    description = models.TextField()
    company = models.CharField(max_length=255)
    company_website = models.URLField(max_length=255)
    company_logo = models.ImageField(upload_to="media/logo")

    posted_by = models.ForeignKey(
        User, related_name="my_jobs", on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    expires = models.DateTimeField(null=True, blank=True)
    applicants = models.ManyToManyField(
        User, related_name="my_applications", blank=True
    )

    fulfilled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} at {self.company}"

    class Meta:
        ordering = ["-created"]

    def get_description_as_markdown(self):
        return mark_safe(markdown(self.description))

