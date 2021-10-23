import datetime

from rest_framework import generics

from .serializers import *

# Для прототипа
today = datetime.date(year=2021, month=10, day=6)


class KPIEntryListView(generics.ListAPIView):
    serializer_class = KPIEntrySerializer
    queryset = KPIEntry.objects.filter(
        date__gte=today-datetime.timedelta(days=7)
    )
    filterset_fields = ["index"]

    def get_queryset(self):
        if "month" in self.request.query_params:
            return KPIEntry.objects.filter(
                date__gte=today-datetime.timedelta(days=30)
            )
        else:
            return KPIEntry.objects.filter(
                date__gte=today-datetime.timedelta(days=7)
            )


class KPIDashboardView(generics.ListAPIView):
    serializer_class = KPIAreaSerializer
    queryset = KPIArea.objects.all()
