from django.shortcuts import redirect, render

from .forms import NewJobForm


def list_jobs(request):
    return render(request, "jobs/list.html")


def post_job(request):
    if request.method == "POST":
        form = NewJobForm(request.POST)

        if form.is_valid():
            return redirect("/")
    else:
        form = NewJobForm()
    return render(request, "jobs/post_job.html", {"form": form})
