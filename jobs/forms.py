from django import forms


from .models import Job


class NewJobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = [
            "posted_by",
            "created",
            "updated",
            "active",
            "expires",
            "applicants",
            "fulfilled",
        ]
