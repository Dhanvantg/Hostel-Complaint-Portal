from django.db import models
from django.contrib.auth.models import User


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
