from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class User(AbstractUser):
    groups = models.ManyToManyField(Group, related_name="car_rental_users", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="car_rental_users")
    email = models.EmailField()
    phone_number = models.CharField(max_length=10)
    address = models.CharField(max_length=255)
    CP = models.CharField(max_length=5)
    city = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.username}"

class Make(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"
    
class Model(models.Model):
    make = models.ForeignKey(Make, on_delete=models.CASCADE, related_name="models")
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.make} {self.name}"
    
class City(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"
    
class Chasis(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"
    
class Car(models.Model):
    make = models.ForeignKey(Make, on_delete=models.CASCADE, related_name="cars")
    model = models.ForeignKey(Model, on_delete=models.CASCADE, related_name="cars")
    year = models.IntegerField()
    chasis = models.ForeignKey(Chasis, on_delete=models.CASCADE, related_name="cars")
    seats = models.IntegerField(validators=[MinValueValidator(2), MaxValueValidator(9)])
    location = models.ForeignKey(City, on_delete=models.CASCADE, related_name="cars")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    licence_plate = models.CharField(max_length=8)
    is_available = models.BooleanField(default=True)
    is_crashed = models.BooleanField(default=False)
    image1 = models.ImageField(upload_to="car_rental/images", blank=True, null=True)
    image2 = models.ImageField(upload_to="car_rental/images", blank=True, null=True)
    image3 = models.ImageField(upload_to="car_rental/images", blank=True, null=True)
    image4 = models.ImageField(upload_to="car_rental/images", blank=True, null=True)
    image5 = models.ImageField(upload_to="car_rental/images", blank=True, null=True)

    def __str__(self):
        return f"{self.model} ({self.year}) in {self.location} for ${self.price} per day ({self.is_available})."

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="bookings")
    start_date = models.DateField()
    total_price = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    home_delivery = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} is booking {self.car} for {self.start_date}"

