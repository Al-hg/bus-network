from django.urls import path
from . import views

app_name = "routes"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:route_id>", views.route_detail, name="route_detail"),
    path("<int:route_id>/book", views.book, name="book"),
    path("<int:route_id>/unbook", views.unbook, name="unbook"),
    path("my_bookings", views.my_bookings, name="my_bookings"),
    
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
]