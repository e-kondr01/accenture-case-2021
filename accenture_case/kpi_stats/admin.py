from django.contrib import admin

from accenture_case.kpi_stats.models import *


class KPIIndexAdmin(admin.ModelAdmin):
    readonly_fields = [
        "get_stdev",
        "actual_value_meets_target"
    ]


admin.site.register(KPIArea)
admin.site.register(KPIIndex, KPIIndexAdmin)
admin.site.register(KPIEntry)
