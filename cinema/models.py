from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    # AbstractUser gives us id, username, first_name, last_name, email, password, is_staff, is_active, etc.
    phone = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=20, default='ROLE_USER')

    def __str__(self):
        return self.username

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Movie(models.Model):
    STATUS_CHOICES = [
        ('NOW_SHOWING', 'Now Showing'),
        ('COMING_SOON', 'Coming Soon'),
    ]
    title = models.CharField(max_length=255)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, related_name='movies')
    language = models.CharField(max_length=50, default='English')
    duration_min = models.IntegerField()
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    synopsis = models.TextField(blank=True, null=True)
    poster_url = models.URLField(max_length=500, blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NOW_SHOWING')

    def __str__(self):
        return self.title

class Screen(models.Model):
    screen_name = models.CharField(max_length=100, unique=True)
    total_rows = models.IntegerField()
    total_columns = models.IntegerField()
    total_seats = models.IntegerField()

    def __str__(self):
        return self.screen_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Generate seats automatically if the screen doesn't have any seats yet
        if not self.seats.exists():
            import string
            alphabet = string.ascii_uppercase
            seats_to_create = []
            
            for r in range(self.total_rows):
                # Handles up to 26 rows (A-Z). For realistic theaters this is plenty.
                row_label = alphabet[r % 26] 
                for c in range(1, self.total_columns + 1):
                    seats_to_create.append(Seat(
                        screen=self,
                        row_label=row_label,
                        seat_number=c,
                        seat_type='STANDARD',
                        is_active=True
                    ))
            
            # Bulk insert the seats to be highly efficient
            if seats_to_create:
                Seat.objects.bulk_create(seats_to_create)

class Seat(models.Model):
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name='seats')
    row_label = models.CharField(max_length=5)
    seat_number = models.IntegerField()
    seat_type = models.CharField(max_length=20, default='STANDARD')
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('screen', 'row_label', 'seat_number')

    def __str__(self):
        return f"{self.screen.screen_name} - {self.row_label}{self.seat_number}"

class Show(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='shows')
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE, related_name='shows')
    show_date = models.DateField()
    show_time = models.TimeField()
    ticket_price = models.DecimalField(max_digits=8, decimal_places=2)
    available_seats = models.IntegerField()
    status = models.CharField(max_length=20, default='SCHEDULED')

    def __str__(self):
        return f"{self.movie.title} on {self.show_date} at {self.show_time}"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    show = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='bookings')
    booking_ref = models.CharField(max_length=30, unique=True)
    total_seats = models.IntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='CONFIRMED')
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.booking_ref

class BookingDetail(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='details')
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"Detail {self.id} for {self.booking.booking_ref}"

class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, default='SUCCESS')
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for {self.booking.booking_ref}"
