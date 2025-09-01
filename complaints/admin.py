from django.contrib import admin
from .models import (
    Profile,
    StaffWhitelist,
    Complaint,
    ComplaintImage,
    ComplaintUpdate,
    Department,
)

admin.site.register(Profile)
admin.site.register(StaffWhitelist)
admin.site.register(Complaint)
admin.site.register(ComplaintImage)
admin.site.register(Department)
admin.site.register(ComplaintUpdate)
