# limits/models.py

from django.db import models

class PeriodLimit(models.Model):
    user_id = models.IntegerField(verbose_name="ID техники", db_index=True)
    date_from = models.DateField(verbose_name="Начало периода", db_index=True)
    date_to = models.DateField(verbose_name="Конец периода")
    period_limit = models.FloatField(verbose_name="Лимит на период", default=0.0)
    new_month_limit = models.FloatField(verbose_name="Накопленный месячный лимит", null=True, blank=True)
    remaining_at_period_end = models.FloatField(verbose_name="Остаток на конец периода", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'period_limits'
        unique_together = ('user_id', 'date_from', 'date_to')
        verbose_name = "Лимит на период"
        verbose_name_plural = "Лимиты на периоды"

    def __str__(self):
        return f"User {self.user_id} {self.date_from}–{self.date_to}"