import logging

from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect

from .forms import BookingForm
from .models import rooms, ROOM_CATEGORY_CHOICES

logger = logging.getLogger(__name__)

PACKAGE_LABELS = dict(
    [
        ('1', 'Bed only'),
        ('2', 'Bed and Breakfast'),
        ('3', 'Half board'),
        ('4', 'Full board'),
        ('5', 'Conference room'),
    ]
)

VALID_CATEGORIES = dict(ROOM_CATEGORY_CHOICES)


def index(request):
    return render(request, 'index.html')


def booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)

        if form.is_valid():
            reservation = form.save()
            send_booking_confirmation_email(reservation)
            return redirect('success')

        # Invalid input (bad email, bad phone, missing date, etc.):
        # re-render the same form with the errors instead of crashing
        # or dumping a stack trace to the visitor.
        return render(request, 'booking.html', {'form': form})

    form = BookingForm()
    return render(request, 'booking.html', {'form': form})


def success(request):
    return render(request, 'success.html')


def check_availability(request):
    """
    Returns how many rooms of the requested category are currently marked
    available in the `rooms` table. This reflects whatever staff has set
    in the admin panel right now — it is NOT date-aware, since rooms
    aren't linked to specific bookings/date ranges in this schema.
    """
    category = request.GET.get('category', '')

    if category not in VALID_CATEGORIES:
        return JsonResponse({'error': 'Unknown category.'}, status=400)

    total = rooms.objects.filter(Room_type=category).count()
    available = rooms.objects.filter(Room_type=category, is_available=True).count()

    return JsonResponse({
        'category': category,
        'available': available,
        'total': total,
    })


def send_booking_confirmation_email(reservation):
    """
    Emails the guest a confirmation of their reservation.
    Any failure here is logged, not shown to the guest — a flaky mail
    server should never make a successful booking look like it failed.
    """
    package_name = PACKAGE_LABELS.get(reservation.Package, reservation.Package)

    subject = 'Your Tulmaat Hotel booking is confirmed'
    message = (
        f"Hi {reservation.Name},\n\n"
        f"Thank you for booking with Tulmaat Hotel! Here are your reservation details:\n\n"
        f"  Check-in date: {reservation.Date.strftime('%d %B %Y')}\n"
        f"  Room category: {reservation.Category}\n"
        f"  Package: {package_name}\n"
        f"  Phone on file: {reservation.Phone}\n\n"
        f"We look forward to welcoming you.\n\n"
        f"Warm regards,\n"
        f"Tulmaat Hotel\n"
    )

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[reservation.Email],
            fail_silently=False,
        )
    except Exception:
        logger.exception('Failed to send booking confirmation email for booking id=%s', reservation.pk)