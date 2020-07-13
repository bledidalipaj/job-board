from django.shortcuts import render


def list_jobs(request):
    return render(request, "jobs/list.html")


def post_job(request):
    return render(request, "jobs/post_job.html")
