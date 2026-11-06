from functools import wraps

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ApplicationForm, ApplicationStatusForm, JobForm, RegistrationForm
from .models import Application, Job, User


def role_required(role):
    def decorator(view):
        @wraps(view)
        @login_required
        def wrapped(request, *args, **kwargs):
            if request.user.role != role:
                return HttpResponseForbidden("You do not have permission to view this page.")
            return view(request, *args, **kwargs)

        return wrapped

    return decorator


def job_list(request):
    jobs = Job.objects.filter(is_active=True)
    query = request.GET.get("q", "").strip()
    location = request.GET.get("location", "").strip()
    category = request.GET.get("category", "").strip()
    company = request.GET.get("company", "").strip()

    if query:
        jobs = jobs.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(company__icontains=query)
            | Q(category__icontains=query)
        )
    if location:
        jobs = jobs.filter(location__icontains=location)
    if category:
        jobs = jobs.filter(category__icontains=category)
    if company:
        jobs = jobs.filter(company__icontains=company)

    return render(
        request,
        "jobs/job_list.html",
        {
            "jobs": jobs,
            "query": query,
            "location": location,
            "category": category,
            "company": company,
        },
    )


def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk, is_active=True)
    already_applied = False
    if request.user.is_authenticated:
        already_applied = Application.objects.filter(job=job, applicant=request.user).exists()
    form = ApplicationForm()

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")
        if request.user.role != User.Role.SEEKER or request.user.is_superuser:
            return HttpResponseForbidden("Only job seekers can apply for jobs.")
        if already_applied:
            messages.info(request, "You have already applied for this job.")
            return redirect("job_detail", pk=job.pk)
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            messages.success(request, "Your application has been submitted.")
            return redirect("job_detail", pk=job.pk)

    return render(
        request,
        "jobs/job_detail.html",
        {"job": job, "form": form, "already_applied": already_applied},
    )


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Your account has been created.")
        return redirect("dashboard")
    return render(request, "registration/register.html", {"form": form})


@login_required
def dashboard(request):
    if request.user.is_superuser:
        return redirect("/admin/")
    if request.user.role == User.Role.EMPLOYER:
        return redirect("employer_jobs")
    return redirect("my_applications")


@role_required(User.Role.SEEKER)
def my_applications(request):
    applications = Application.objects.filter(applicant=request.user).select_related("job")
    return render(request, "jobs/my_applications.html", {"applications": applications})


@role_required(User.Role.EMPLOYER)
def employer_jobs(request):
    jobs = Job.objects.filter(employer=request.user)
    return render(request, "jobs/employer_jobs.html", {"jobs": jobs})


@role_required(User.Role.EMPLOYER)
def job_create(request):
    form = JobForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        job = form.save(commit=False)
        job.employer = request.user
        job.save()
        messages.success(request, "Your job listing has been created.")
        return redirect("employer_jobs")
    return render(request, "jobs/job_form.html", {"form": form, "heading": "Post a job"})


@role_required(User.Role.EMPLOYER)
def job_edit(request, pk):
    job = get_object_or_404(Job, pk=pk, employer=request.user)
    form = JobForm(request.POST or None, instance=job)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Your job listing has been updated.")
        return redirect("employer_jobs")
    return render(request, "jobs/job_form.html", {"form": form, "heading": "Edit job"})


@role_required(User.Role.EMPLOYER)
@require_POST
def job_delete(request, pk):
    job = get_object_or_404(Job, pk=pk, employer=request.user)
    job.delete()
    messages.success(request, "Your job listing has been deleted.")
    return redirect("employer_jobs")


@role_required(User.Role.EMPLOYER)
def employer_applications(request):
    applications = Application.objects.filter(job__employer=request.user).select_related(
        "job", "applicant"
    )
    return render(request, "jobs/employer_applications.html", {"applications": applications})


@role_required(User.Role.EMPLOYER)
@require_POST
def application_update(request, pk):
    application = get_object_or_404(Application, pk=pk, job__employer=request.user)
    form = ApplicationStatusForm(request.POST, instance=application)
    if form.is_valid():
        form.save()
        messages.success(request, "Application status updated.")
    else:
        messages.error(request, "Choose a valid application status.")
    return redirect("employer_applications")


@require_POST
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("job_list")
