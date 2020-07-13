from django.urls import path

from . import views

urlpatterns = [
    path("", views.list_jobs, name="list_jobs"),
    path("post_job/", views.post_job, name="post_job"),
]

