from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from decimal import Decimal, InvalidOperation
from datetime import date

from .models import User, Make, City, Car, Booking, Model, Chasis
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.

def index(request):
    return render(request, "car_rental/index.html")

def landing(request):
    return render(request, "car_rental/landing.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "car_rental/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "car_rental/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        telephone_number = request.POST["phone"]
        address = request.POST["address"]
        CP = request.POST["CP"]
        city = request.POST["city"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        # Ensure password matches confirmation
        if password != confirmation:
            return render(request, "car_rental/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create a new user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.phone_number = telephone_number
        user.address = address
        user.CP = CP
        user.city = city
        user.save()
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "car_rental/register.html")

def search_cars(request):
    cities = City.objects.all()
    makes = Make.objects.all()
    city_name = request.GET.get('city', '').capitalize()
    make_name = request.GET.get('make', '').capitalize()
    year = request.GET.get('year')
    min_price = request.GET.get('min-price')
    max_price = request.GET.get('max-price')
    cars = Car.objects.all()
    if city_name:
        try:
            city = City.objects.get(name__iexact=city_name)
            cars = cars.filter(location=city)
        except City.DoesNotExist:
            cars = Car.objects.none()
    if make_name:
        try:
            make = Make.objects.get(name__iexact=make_name)
            cars = cars.filter(make=make)
        except Make.DoesNotExist:
            cars = Car.objects.none()
    if year:
        try:
            year = int(year)
            cars = cars.filter(year=year)
        except ValueError:
            pass
    if min_price:
        try:
            min_price = Decimal(min_price.replace(',', '').replace('$', ''))
            cars = cars.filter(price__gte=min_price)
        except InvalidOperation:
            pass
    if max_price:
        try:
            max_price = Decimal(max_price.replace(',', '').replace('$', ''))
            cars = cars.filter(price__lte=max_price)
        except InvalidOperation:
            pass
    if min_price and max_price and min_price > max_price:
        cars = Car.objects.none()
    return render(request, "car_rental/search.html", {
        "cars": cars,
        "selected_city": city_name,
        "selected_make": make_name,
        "selected_year": year,
        "min_price": min_price if min_price else '',
        "max_price": max_price if max_price else '',
        "cities": cities,
        "makes": makes,
    })

def profile(request, username):
    user = get_object_or_404(User, username=username)
    bookings = Booking.objects.filter(user=user)
    return render(request, 'car_rental/profile.html', {
        'user': user,
        'bookings': bookings,
    })

def load_car(request, licence_plate):
    car = Car.objects.get(licence_plate=licence_plate)
    return render(request, 'car_rental/cars.html', {
        'car': car,
    })

def book_car(request, licence_plate):
    if request.method == 'POST':
        user = get_object_or_404(User, pk=request.user.pk)
        if not isinstance(user, User):
            return render(request, 'car_rental/book.html', {
                'error': 'User instance mismatch.'
            })
        car = get_object_or_404(Car, licence_plate=licence_plate)
        start_date = request.POST.get('start_date')
        if start_date < str(date.today()):
            return render(request, 'car_rental/book.html', {
                'car': car,
                'error': 'Invalid date. Please select a future date.'
            })
        if car.bookings.filter(start_date=start_date).exists():
            return render(request, 'car_rental/book.html', {
                'car': car,
                'error': 'Car already booked for this date.'
            })
        total_price = car.price
        booking = Booking(user=user, car=car, start_date=start_date, total_price=total_price)
        booking.save()
        return HttpResponseRedirect(reverse('profile', args=[user.username]))
    else:
        car = get_object_or_404(Car, licence_plate=licence_plate)
        return render(request, 'car_rental/book.html', {
            'car': car,
        })
    
def edit_profile(request, username):
    user = get_object_or_404(User, username=username)
    if user.username != request.user.username:
        return HttpResponseForbidden("ERROR 403: You are not authorized to edit this profile.", status=403)
    if request.method == 'POST':
        user.email = request.POST.get('email')
        user.phone_number = request.POST.get('phone_number')
        user.address = request.POST.get('address')
        user.CP = request.POST.get('CP')
        user.city = request.POST.get('city')
        user.save()
        return HttpResponseRedirect(reverse('profile', args=[user.username]))
    return render(request, 'car_rental/edit_profile.html', {
        'user': user,
    })

def staff(request):
    return render(request, 'car_rental/staff.html')

@staff_member_required
def delete_profile(request, username):
    user = get_object_or_404(User, username=username)
    user.delete()
    return HttpResponseRedirect(reverse('staff'))

def get_users(request):
    users = User.objects.all().values('username', 'first_name', 'last_name', 'email', 'phone_number', 'address', 'city', 'CP')
    users_list = list(users)
    return JsonResponse({"users": users_list})


def get_cars(request):
    cars = Car.objects.all().values('make', 'model', 'year', 'chasis', 'seats', 'location', 'price', 'licence_plate', 'is_available', 'is_crashed', 'image1', 'image2', 'image3', 'image4', 'image5')
    cars_list = list(cars)
    return JsonResponse({"cars": cars_list})