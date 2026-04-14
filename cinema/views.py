from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Movie, Show, Screen, Seat, Booking, BookingDetail, Payment, User
from django.utils import timezone
import uuid

def home(request):
    movies = Movie.objects.filter(status='NOW_SHOWING')
    context = {'movies': movies}
    return render(request, 'cinema/home.html', context)

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    shows = movie.shows.filter(show_date__gte=timezone.now().date()).order_by('show_date', 'show_time')
    context = {'movie': movie, 'shows': shows}
    return render(request, 'cinema/movie_detail.html', context)

@login_required
def show_seats(request, show_id):
    show = get_object_or_404(Show, id=show_id)
    screen = show.screen
    seats = screen.seats.filter(is_active=True).order_by('row_label', 'seat_number')
    
    # Get booked seats for this show
    booked_details = BookingDetail.objects.filter(booking__show=show, booking__status='CONFIRMED')
    booked_seat_ids = [detail.seat_id for detail in booked_details]

    # Organize seats by row for the template
    row_dict = {}
    for seat in seats:
        seat.is_booked = seat.id in booked_seat_ids
        if seat.row_label not in row_dict:
            row_dict[seat.row_label] = []
        row_dict[seat.row_label].append(seat)
    
    context = {
        'show': show,
        'row_dict': row_dict,
    }
    return render(request, 'cinema/seats.html', context)

@login_required
def checkout(request):
    if request.method == 'POST':
        show_id = request.POST.get('show_id')
        seat_ids = request.POST.getlist('seats[]')
        
        if not seat_ids:
            messages.error(request, 'Please select at least one seat.')
            return redirect('show_seats', show_id=show_id)
            
        show = get_object_or_404(Show, id=show_id)
        selected_seats = Seat.objects.filter(id__in=seat_ids)
        total_amount = len(selected_seats) * show.ticket_price
        
        # Create Booking
        booking = Booking.objects.create(
            user=request.user,
            show=show,
            booking_ref=str(uuid.uuid4().hex[:8].upper()),
            total_seats=len(selected_seats),
            total_amount=total_amount,
            status='CONFIRMED'
        )
        
        # Create Booking Details
        for seat in selected_seats:
            BookingDetail.objects.create(
                booking=booking,
                seat=seat,
                price=show.ticket_price
            )
            
        # Create Mock Payment
        Payment.objects.create(
            booking=booking,
            amount=total_amount,
            payment_method='CARD',
            transaction_id='TXN' + str(uuid.uuid4().hex[:10].upper())
        )
        
        messages.success(request, f'Booking Successful! Ref: {booking.booking_ref}')
        return redirect('my_bookings')
        
    return redirect('home')

@login_required
def my_bookings(request):
    bookings = request.user.bookings.all().order_by('-booked_at')
    return render(request, 'cinema/my_bookings.html', {'bookings': bookings})

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')
        full_name = request.POST.get('full_name')
        
        if password != confirm:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'cinema/register.html')
            
        if User.objects.filter(username=email).exists():
            messages.error(request, 'Account with this email already exists.')
            return render(request, 'cinema/register.html')
            
        user = User.objects.create_user(username=email, email=email, password=password, first_name=full_name)
        user.role = 'ROLE_USER'
        user.save()
        
        login(request, user)
        messages.success(request, 'Account created successfully!')
        return redirect('home')
        
    return render(request, 'cinema/register.html')
