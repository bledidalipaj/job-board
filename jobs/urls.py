from django.urls import path

from . import views

urlpatterns = [
    path("", views.ListJobsView.as_view(), name="list_jobs"),
    path("job/<int:pk>/", views.JobDetailView.as_view(), name="job_detail"),
    path("job/<int:pk>/update/", views.JobUpdateView.as_view(), name="job_update"),
    path("job/<int:pk>/delete/", views.JobDeleteView.as_view(), name="job_delete"),
    path("post_job/", views.post_job, name="post_job"),
]
