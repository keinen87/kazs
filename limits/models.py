# limits/models.py

from django.db import models
from report_app.models import Users


class WeekLimit(models.Model):
    user_id = models.IntegerField(verbose_name="ID техники", db_index=True)
    week_start = models.DateField(verbose_name="Начало недели", db_index=True)
    week_end = models.DateField(verbose_name="Конец недели")
    weekly_limit = models.FloatField(verbose_name="Недельный лимит", default=0.0)
    new_month_limit = models.FloatField(verbose_name="Новый месячный лимит (накопленный)", null=True, blank=True)
    week_remaining = models.FloatField(verbose_name="Остаток на конец недели", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'week_limits'
        unique_together = ('user_id', 'week_start')
        verbose_name = "Недельный лимит"
        verbose_name_plural = "Недельные лимиты"

    def __str__(self):
        try:
            user = Users.objects.get(id=self.user_id)
            return f"{user.full_name} – {self.week_start}"
        except Users.DoesNotExist:
            return f"User {self.user_id} – {self.week_start}"