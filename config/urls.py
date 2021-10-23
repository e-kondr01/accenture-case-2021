from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from accenture_case.kpi_stats.views import *
from accenture_case.whouse_problems.views import *


urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("api/kpi-entries", KPIEntryListView.as_view()),
    path("api/kpi-dashboard", KPIDashboardView.as_view()),
    path("api/problem-finder", ProblemFinderView.as_view())
]

if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
