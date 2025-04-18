from django.urls import path
from . import views

app_name = 'attendance' 
urlpatterns = [
    path("generate-code/", views.generate_code, name="generate_code"),
    path("mark-attendance/", views.mark_attendance, name="mark_attendance"),
    path('list/<str:code>/',views.attendance_list,name='attendance_list'),
    path("created-sheets/",views.attendance_sheets_created,name="attendance_sheets_created"),
    path("marked-attendance/",views.attendance_marked_by_user, name="attendance_marked_by_user"),
]
