from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import AttendanceCode, AttendanceRecord
from django.contrib.auth.decorators import login_required
import random

from django.utils.timezone import now, timedelta

@login_required
def generate_code(request):
    latest_code = AttendanceCode.objects.filter(created_by=request.user).order_by('-created_at').first()
    
    if request.method == "POST":
        code = str(random.randint(100000, 999999))
        created_at = now()
        expiry_time = created_at + timedelta(seconds=90)

        # Create the code in the database
        AttendanceCode.objects.create(
            code=code,
            created_by=request.user,
            created_at=created_at
        )
        
        # Refresh the latest_code after creating a new one
        latest_code = AttendanceCode.objects.filter(created_by=request.user).order_by('-created_at').first()

        # Return the code and expiry time
        return JsonResponse({
            "code": code,
            "expiry_time": expiry_time.strftime("%Y-%m-%d %H:%M:%S")
        })

    # Render template for GET requests
    return render(request, "attendance/generate_code.html", {
        "user": request.user,
        "latest_code": latest_code.code if latest_code else None,
    })


@login_required
def mark_attendance(request):
    if request.method == "POST":
        code = request.POST.get("code")
        attendance_code = get_object_or_404(AttendanceCode, code=code)
        
        # Check if the code is still valid
        if attendance_code.is_active and (now() - attendance_code.created_at).total_seconds() <= 90:
            AttendanceRecord.objects.create(user=request.user, attendance_code=attendance_code)
            return JsonResponse({"status": "success"})
        else:
            return JsonResponse({"status": "failed", "error": "Code expired or invalid."})
    return render(request, "attendance/mark_attendance.html")

@login_required
def attendance_list(request, code):
    # Fetch the AttendanceCode object created by the logged-in user with the given code
    attendance_code = get_object_or_404(AttendanceCode, code=code, created_by=request.user)
    
    # Fetch the related attendance records using the correct related_name
    attendance_records = attendance_code.attendance_records.all()

    # Render the attendance list page
    return render(request, 'attendance/attendance_list.html', {
        'attendance_code': attendance_code,
        'attendance_records': attendance_records,
    })
