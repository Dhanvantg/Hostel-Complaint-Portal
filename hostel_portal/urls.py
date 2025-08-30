from django.contrib import admin
from django.urls import path, include
from complaints.views import HomePageView, DashboardView  # Import DashboardView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
]
