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

class AttendanceSheet(models.Model):
    id = models.AutoField(primary_key=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_sheets")
    created_at = models.DateTimeField(default=now)
    students_marked = models.ManyToManyField(User, related_name="marked_sheets", blank=True)

    def __str__(self):
        return f"sheet by {self.created_by.username} on {self.created_at}"
    

class MarkedAttendanceModel(models.Model):
    id = models.AutoField(primary_key=True)
    attendance_sheet = models.ForeignKey(
        AttendanceSheet, on_delete=models.CASCADE, related_name="marked_attendances"
    )
    marked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="marked_records")
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="student_attendances")
    timestamp = models.DateTimeField(default=now)
    status  = models.BooleanField(default=True)

    def save(self, *args,**kwargs):
        super().save(*args, **kwargs)
        self.attendance_sheet.students_marked.add(self.student)

    def __str__(self):
        return f"{self.student.username} - {self.status} - {self.marked_by.username}"