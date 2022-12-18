from django.db import models
from django.utils.timezone import localtime


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )

    def get_duration(self):
        current_time = localtime(self.leaved_at).replace(microsecond=0)
        entered_time = localtime(self.entered_at).replace(microsecond=0)
        return current_time - entered_time

    @staticmethod
    def format_duration(duration):
        total_seconds = int(duration.total_seconds())
        hours, remainder = divmod(total_seconds, 60 * 60)
        minutes, _ = divmod(remainder, 60)
        return f'{hours if hours else "0"}час. {minutes if minutes else "0"}мин.'

    def is_visit_long(self, minutes=60):
        visit_duration = self.get_duration().total_seconds() // 60
        return visit_duration > minutes
