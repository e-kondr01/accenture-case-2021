from django.db import models
from statistics import stdev
from typing import Optional


class KPIArea(models.Model):
    """Модель область КПЭ"""

    name = models.CharField(
        max_length=256,
        verbose_name="название"
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "область КПЭ"
        verbose_name_plural = "области КПЭ"


class KPIIndex(models.Model):
    """Модель показателя КПЭ"""

    area = models.ForeignKey(
        to=KPIArea,
        on_delete=models.CASCADE,
        related_name="indexes",
        verbose_name="область КПЭ"
    )

    name = models.CharField(
        max_length=256,
        verbose_name="название"
    )

    description = models.TextField(
        max_length=2048,
        verbose_name="описание"
    )

    target_value = models.PositiveSmallIntegerField(
        verbose_name="целевое значние (в процентах)"
    )

    is_target_value_more = models.BooleanField(
        default=True,
        verbose_name="целевое значение должно быть больше?"
    )

    def get_actual_value(self) -> Optional[int]:
        actual_entry: "KPIEntry" = self.entries.order_by(
            "-date"
        ).first()
        if actual_entry:
            return actual_entry.value
        else:
            return 0

    def get_previous_value(self) -> int:
        previous_entries = self.entries.order_by(
            "-date"
        )
        if len(previous_entries) > 1:
            return previous_entries[1].value
        else:
            return 0

    def actual_value_change(self) -> int:
        return abs(self.get_actual_value() - self.get_previous_value())

    def actual_value_rise(self) -> bool:
        return self.get_actual_value() > self.get_previous_value()

    def actual_value_meets_target(self) -> bool:
        actual_entry: "KPIEntry" = self.entries.order_by(
            "-date"
        ).first()
        if actual_entry:
            return actual_entry.meets_target()
        else:
            return False

    def get_values_list(self) -> list[int]:
        res: list = []
        for entry in self.entries.all():
            res.append(entry.value)
        return res

    def get_diffs_list(self) -> list[int]:
        res: list = []
        values_list = self.get_values_list()
        for i in range(1, len(values_list)):
            res.append(
                values_list[i] - values_list[i-1]
            )
        return res

    def get_stdev(self) -> float:
        diffs = self.get_diffs_list()
        st_dev = stdev(diffs)
        return st_dev

    def actual_value_drastic_change(self) -> bool:
        actual_entry: "KPIEntry" = self.entries.order_by(
            "-date"
        ).first()
        if actual_entry:
            return actual_entry.is_drastic_change()
        else:
            return False

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "показатель КПЭ"
        verbose_name_plural = "показатели КПЭ"


class KPIEntry(models.Model):
    """Значение показателя КПЭ за конкретную дату"""

    index: KPIIndex = models.ForeignKey(
        to=KPIIndex,
        on_delete=models.CASCADE,
        related_name="entries",
        verbose_name="показатель КПЭ"
    )

    date = models.DateField(
        verbose_name="дата"
    )

    value = models.PositiveSmallIntegerField(
        verbose_name="значение (в процентах)"
    )

    def meets_target(self) -> bool:
        """Выполняется ли целевое значение?"""
        if self.index.is_target_value_more:
            return self.value > self.index.target_value
        else:
            return self.value < self.index.target_value

    def get_diff(self) -> Optional[int]:
        previous_entry = self.index.entries.filter(
            date__lt=self.date
        ).order_by(
            "-date"
        ).first()
        if previous_entry:
            return abs(previous_entry.value - self.value)
        else:
            return None

    def is_drastic_change(self) -> bool:
        """Сильное отклонение в значении"""
        st_dev = self.index.get_stdev()
        if self.get_diff():
            return self.get_diff() > 2 * st_dev
        else:
            return False

    def __str__(self) -> str:
        return f"{self.value}% {self.index} {self.date}"

    class Meta:
        verbose_name = "значение показателя КПЭ"
        verbose_name_plural = "значения показателя КПЭ"
        ordering = ["date"]
