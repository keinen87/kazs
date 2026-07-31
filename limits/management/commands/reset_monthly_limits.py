from django.core.management.base import BaseCommand
from report_app.models import Users
from datetime import datetime
import calendar

class Command(BaseCommand):
    help = 'Сбрасывает месячные лимиты пользователей до 1 литра в последний день месяца.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user_id',
            type=int,
            help='ID пользователя для тестирования (если не указан, обновляются все)',
        )

    def handle(self, *args, **options):
        user_id = options.get('user_id')
        today = datetime.now().date()
        last_day = calendar.monthrange(today.year, today.month)[1]

        # Если сегодня не последний день месяца и не указан user_id – пропускаем
        if today.day != last_day and user_id is None:
            self.stdout.write(f"Сегодня не последний день месяца ({today.day}/{last_day}), пропускаем.")
            return

        if user_id:
            # Обновляем конкретного пользователя через update (без вызова save)
            updated = Users.objects.using('default').filter(id=user_id).update(month_limit=1)
            if updated:
                user = Users.objects.using('default').get(id=user_id)
                self.stdout.write(f"✅ Для пользователя {user.full_name} (ID {user_id}) month_limit установлен в 1.")
            else:
                self.stdout.write(f"⚠️ Пользователь с ID {user_id} не найден.")
            return

        # Обновляем всех пользователей
        updated = Users.objects.using('default').all().update(month_limit=1)
        self.stdout.write(f"✅ Обновлено {updated} пользователей (month_limit = 1) в последний день месяца.")

        # Логирование
        try:
            with open('/var/log/limits_reset.log', 'a') as f:
                f.write(f"{datetime.now().isoformat()} - Limits reset successful, {updated} users updated.\n")
        except Exception as e:
            self.stdout.write(f"⚠️ Не удалось записать лог: {e}")