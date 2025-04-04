from django.urls import path
from .views import register, login_view, home, landing_page, logout_view

app_name= "users"
urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('home/', home, name='home'),
    path('logout/', logout_view, name='logout'),
    
]
    