from django.contrib import admin
from .models import User, Make, Model, City, Car, Booking, Chasis

# Register your models here.
admin.site.register(User)
admin.site.register(Make)
admin.site.register(Model)
admin.site.register(City)
admin.site.register(Car)
admin.site.register(Booking)
admin.site.register(Chasis)
