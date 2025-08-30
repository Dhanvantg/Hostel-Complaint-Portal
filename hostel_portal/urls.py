from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from complaints.views import (
    HomePageView,
    DashboardView,
    ComplaintListView,
    ComplaintCreateView,
    ComplaintDetailView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", HomePageView.as_view(), name="home"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("complaints/", ComplaintListView.as_view(), name="complaint-list"),
    path("complaint/new/", ComplaintCreateView.as_view(), name="complaint-create"),
    path("complaint/<int:pk>/", ComplaintDetailView.as_view(), name="complaint-detail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
