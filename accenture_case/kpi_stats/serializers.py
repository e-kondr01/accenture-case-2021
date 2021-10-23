from rest_framework import serializers

from accenture_case.kpi_stats.models import *


class KPIEntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = KPIEntry
        fields = [
            "id",
            "date",
            "value",
            "is_drastic_change"
        ]


class KPIIndexSerializer(serializers.ModelSerializer):

    class Meta:
        model = KPIIndex
        fields = [
            "id",
            "name",
            "description",
            "target_value_with_sign",
            "get_actual_value",
            "actual_value_drastic_change",
            "value_difference",
            "actual_value_rise",
            "actual_value_meets_target"
        ]


class KPIAreaSerializer(serializers.ModelSerializer):
    indexes = KPIIndexSerializer(many=True, read_only=True)

    class Meta:
        model = KPIArea
        fields = [
            "id",
            "name",
            "indexes"
        ]
