from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import NewJobForm


def list_jobs(request):
    return render(request, "jobs/list.html")


@login_required
def post_job(request):
    if request.method == "POST":
        form = NewJobForm(request.POST, request.FILES)

        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user

            job.save()
            return redirect("/")
    else:
        form = NewJobForm()
    return render(request, "jobs/post_job.html", {"form": form})
