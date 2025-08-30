from django.contrib import admin
from .models import Profile, StaffWhitelist, Complaint, ComplaintImage, Department

admin.site.register(Profile)
admin.site.register(StaffWhitelist)
admin.site.register(Complaint)
admin.site.register(ComplaintImage)
admin.site.register(Department)
