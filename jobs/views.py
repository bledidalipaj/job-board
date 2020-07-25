from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView, UpdateView

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


class JobDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Job
    success_url = reverse_lazy("list_jobs")

    def test_func(self):
        job = self.get_object()

        if self.request.user == job.posted_by:
            return True
        return False


class JobDetailView(DetailView):
    model = Job
    template_name = "jobs/detail.html"


class JobUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Job
    form_class = NewJobForm
    template_name = "jobs/create_update_job.html"

    def test_func(self):
        job = self.get_object()

        if self.request.user == job.posted_by:
            return True
        return False


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
    return render(request, "jobs/create_update_job.html", {"form": form})
