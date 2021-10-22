from rest_framework import serializers

from accenture_case.kpi_stats.models import *


class KPIEntrySerializer(serializers.ModelSerializer):

    class Meta:
        model = KPIEntry
        fields = [
            "id",
            "date",
            "value",
            "meets_target"
        ]


class KPIIdexSerializer(serializers.ModelSerializer):

    class Meta:
        model = KPIIndex
        fields = [
            "id",
            "name",
            "description",
            "get_actual_value",
            "actual_value_meets_target"
        ]


class KPIAreaSerializer(serializers.ModelSerializer):
    indexes = KPIIdexSerializer(many=True, read_only=True)

    class Meta:
        model = KPIArea
        fields = [
            "id",
            "name",
            "indexes"
        ]
