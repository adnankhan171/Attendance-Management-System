from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now, timedelta

class AttendanceCode(models.Model):
    code = models.CharField(max_length=6, unique=True)
    created_by = models.ForeignKey(User,
                                   on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now)
    is_active = models.BooleanField(default=True)

    def is_valid(self):
        """Check if the code is still valid (within 90 seconds)."""
        return self.is_active and (now() - self.created_at).total_seconds() <= 90

    def __str__(self):
        return self.code
    
    
class AttendanceRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attendance_code = models.ForeignKey(AttendanceCode,
                                        on_delete=models.CASCADE,
                                        related_name = 'attendance_records')
    timestamp = models.DateTimeField(default=now)
    
    def __str__(self):
        return f"{self.user.username} - {self.attendance_code.code}"
