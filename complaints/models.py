from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    class Role(models.TextChoices):
        STUDENT = "STUDENT", "Student"
        STAFF = "STAFF", "Staff"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STUDENT)

    student_id = models.CharField(max_length=20, blank=True, null=True, unique=True)
    hostel = models.CharField(max_length=50, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} - {self.get_role_display()}"


class StaffWhitelist(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Complaint(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        ONGOING = "ONGOING", "Ongoing"
        RESOLVED = "RESOLVED", "Resolved"

    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="complaints"
    )
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.PENDING
    )
    created_at = models.DateTimeField(default=timezone.now)
    staff_remarks = models.TextField(blank=True, null=True)
    resolved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="resolved_complaints",
    )

    def __str__(self):
        return f"{self.title} by {self.student.email}"


def get_complaint_image_path(instance, filename):
    return f"complaints/{instance.complaint.id}/{filename}"


class ComplaintImage(models.Model):
    complaint = models.ForeignKey(
        Complaint, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to=get_complaint_image_path)

    def __str__(self):
        return f"Image for complaint {self.complaint.id}"


class ComplaintUpdate(models.Model):
    complaint = models.ForeignKey(
        Complaint, on_delete=models.CASCADE, related_name="updates"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    update_text = models.TextField()

    class Meta:
        ordering = ["-timestamp"]
