from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    DetailView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.db.models import Q
from django_ratelimit.decorators import ratelimit
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
    paginate_by = 2

    def get_queryset(self):
        # First, determine the base queryset based on the user's role.
        if self.request.user.profile.role == Profile.Role.STUDENT:
            base_queryset = Complaint.objects.filter(student=self.request.user)
        else:
            # Staff can see all complaints.
            base_queryset = Complaint.objects.all()
        # Then, get the search query from the URL's GET parameters.
        query = self.request.GET.get("q")
        if query:
            # If a query exists, filter the base queryset.
            search_queryset = base_queryset.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
            return search_queryset.order_by("-created_at")

        # If no search query, return the ordered base queryset.
        return base_queryset.order_by("-created_at")


@method_decorator(ratelimit(key="user", rate="5/h", block=True), name="dispatch")
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
            if updated_complaint.status == Complaint.Status.RESOLVED:
                self.send_resolution_email(updated_complaint)

        return redirect(reverse("complaint-detail", kwargs={"pk": complaint.pk}))

    def send_resolution_email(self, complaint):
        """A helper method to render and send the email."""
        context = {"complaint": complaint}

        subject = render_to_string(
            "emails/complaint_resolved_subject.txt", context
        ).strip()
        body = render_to_string("emails/complaint_resolved_body.txt", context)

        send_mail(
            subject=subject,
            message=body,
            from_email=None,  # Will use DEFAULT_FROM_EMAIL from settings
            recipient_list=[complaint.student.email],
            fail_silently=False,
        )
