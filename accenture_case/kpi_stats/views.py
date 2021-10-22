from rest_framework import generics

from .serializers import *


class KPIEntryListView(generics.ListAPIView):
    serializer_class = KPIEntrySerializer
    queryset = KPIEntry.objects.all()
    filterset_fields = ["index", "date"]


class KPIDashboardView(generics.ListAPIView):
    serializer_class = KPIAreaSerializer
    queryset = KPIArea.objects.all()
