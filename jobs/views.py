from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.generic import ListView

from .forms import NewJobForm
from .models import Job


class ListJobsView(ListView):
    context_object_name = "jobs"
    model = Job
    paginate_by = 2
    template_name = "jobs/list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        job_type = self.request.GET.get("job_type")

        if job_type:
            context["job_type"] = job_type
        return context

    def get_queryset(self, **kwargs):
        # get query string
        job_type = self.request.GET.get("job_type")

        if job_type:
            return Job.objects.filter(job_type=job_type)
        return Job.objects.all()


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
