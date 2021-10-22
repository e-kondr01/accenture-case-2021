from django.db import models


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

    def get_actual_value(self) -> int:
        actual_entry: "KPIEntry" = self.entries.order_by(
            "-date"
        ).first()
        return actual_entry.value

    def actual_value_meets_target(self) -> bool:
        actual_entry: "KPIEntry" = self.entries.order_by(
            "-date"
        ).first()
        return actual_entry.meets_target()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "показатель КПЭ"
        verbose_name_plural = "показатели КПЭ"


class KPIEntry(models.Model):
    """Значение показателя КПЭ за конкретную дату"""

    index = models.ForeignKey(
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

    def __str__(self) -> str:
        return f"{self.value}% {self.index} {self.date}"

    class Meta:
        verbose_name = "значение показателя КПЭ"
        verbose_name_plural = "значения показателя КПЭ"
        ordering = ["date"]
