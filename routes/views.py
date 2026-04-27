from django.shortcuts import render
from .models import Route, Station

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse


def index(request):
    routes = Route.objects.all()
    
    return render(request, "routes/index.html", {
        "routes": routes
    })

def route_detail(request, route_id):
    route = Route.objects.get(pk=route_id)
    passengers = route.passengers.all()
    
    is_booked = False
    if request.user.is_authenticated:
        if request.user in passengers:
            is_booked = True

    return render(request, "routes/route_detail.html", {
        "route": route,
        "passengers": passengers,
        "is_booked": is_booked 
    })


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("routes:index")) # توجيهه للصفحة الرئيسية
        else:
            return render(request, "routes/login.html", {
                "message": "اسم المستخدم أو كلمة المرور غير صحيحة."
            })
    else:
        return render(request, "routes/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("routes:login"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "routes/register.html", {
                "message": "كلمات المرور غير متطابقة."
            })

        try:
            user = User.objects.create_user(username, email="", password=password)
            user.save()
        except IntegrityError:
            return render(request, "routes/register.html", {
                "message": "اسم المستخدم هذا محجوز مسبقاً."
            })
        
        login(request, user)
        return HttpResponseRedirect(reverse("routes:index"))
    else:
        return render(request, "routes/register.html")
    


def book(request, route_id):
    if request.method == "POST":
        route = Route.objects.get(pk=route_id)
        route.passengers.add(request.user)
        return HttpResponseRedirect(reverse("routes:route_detail", args=(route.id,)))

def unbook(request, route_id):
    if request.method == "POST":
        route = Route.objects.get(pk=route_id)
        route.passengers.remove(request.user)
        return HttpResponseRedirect(reverse("routes:route_detail", args=(route.id,)))
    

def my_bookings(request):
    # التأكد أن المستخدم مسجل دخول، وإذا لم يكن، نوجهه لصفحة الدخول
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("routes:login"))

    # جلب جميع الرحلات التي قام المستخدم الحالي بحجزها
    # استخدمنا booked_routes لأنك حددتها في الـ related_name في الموديل
    user_bookings = request.user.booked_routes.all()

    return render(request, "routes/my_bookings.html", {
        "bookings": user_bookings
    })