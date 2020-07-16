from django.urls import path

from . import views

urlpatterns = [
    path("", views.ListJobsView.as_view(), name="list_jobs"),
    path("post_job/", views.post_job, name="post_job"),
]
