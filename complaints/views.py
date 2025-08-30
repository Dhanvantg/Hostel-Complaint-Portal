from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    DetailView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from .models import Profile, Complaint, ComplaintImage
from .forms import ComplaintForm, StaffUpdateForm


class HomePageView(TemplateView):
    template_name = "home.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard")
        return super().dispatch(request, *args, **kwargs)


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"


class ComplaintListView(LoginRequiredMixin, ListView):
    model = Complaint
    template_name = "complaints/complaint_list.html"
    context_object_name = "complaints"

    def get_queryset(self):
        if self.request.user.profile.role == Profile.Role.STUDENT:
            return Complaint.objects.filter(student=self.request.user).order_by(
                "-created_at"
            )
        return Complaint.objects.all().order_by("-created_at")


class ComplaintCreateView(LoginRequiredMixin, CreateView):
    model = Complaint
    form_class = ComplaintForm
    template_name = "complaints/complaint_form.html"
    success_url = reverse_lazy("complaint-list")

    def form_valid(self, form):
        form.instance.student = self.request.user
        complaint = form.save()

        images = self.request.FILES.getlist("images")
        for image in images:
            ComplaintImage.objects.create(complaint=complaint, image=image)

        return super().form_valid(form)


class ComplaintDetailView(LoginRequiredMixin, DetailView):
    model = Complaint
    template_name = "complaints/complaint_detail.html"
    context_object_name = "complaint"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the staff update form to the context if the user is staff/admin
        if self.request.user.profile.role == Profile.Role.STAFF:
            context["staff_form"] = StaffUpdateForm(instance=self.get_object())
        return context

    def post(self, request, *args, **kwargs):
        # This method handles the form submission from staff
        if request.user.profile.role != Profile.Role.STAFF:
            return redirect("home")

        complaint = self.get_object()
        form = StaffUpdateForm(request.POST, instance=complaint)

        if form.is_valid():
            updated_complaint = form.save(commit=False)
            # If the status is changed to 'Resolved', set the 'resolved_by' user
            if (
                form.cleaned_data["status"] == Complaint.Status.RESOLVED
                and complaint.status != Complaint.Status.RESOLVED
            ):
                updated_complaint.resolved_by = request.user
            updated_complaint.save()

        return redirect(reverse("complaint-detail", kwargs={"pk": complaint.pk}))
