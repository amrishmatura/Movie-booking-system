from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Genre, Movie, Screen, Seat, Show, Booking, BookingDetail, Payment

admin.site.register(User, UserAdmin)
admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(Screen)
admin.site.register(Seat)
admin.site.register(Show)
admin.site.register(Booking)
admin.site.register(BookingDetail)
admin.site.register(Payment)
