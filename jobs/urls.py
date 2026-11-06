from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.job_list, name="job_list"),
    path("jobs/<int:pk>/", views.job_detail, name="job_detail"),
    path("register/", views.register, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("my-applications/", views.my_applications, name="my_applications"),
    path("employer/jobs/", views.employer_jobs, name="employer_jobs"),
    path("employer/jobs/new/", views.job_create, name="job_create"),
    path("employer/jobs/<int:pk>/edit/", views.job_edit, name="job_edit"),
    path("employer/jobs/<int:pk>/delete/", views.job_delete, name="job_delete"),
    path("employer/applications/", views.employer_applications, name="employer_applications"),
    path(
        "employer/applications/<int:pk>/update/",
        views.application_update,
        name="application_update",
    ),
]
