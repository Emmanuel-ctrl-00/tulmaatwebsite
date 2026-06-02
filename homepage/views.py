from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import bookings

# Create your views here.
def booking(request):
    if request.method == 'POST':
        form = bookings(request.POST)

        name_data = request.POST.get('Name')
        email_data = request.POST.get('Email')
        phone_data = request.POST.get('Phone')
        date_data = request.POST.get('Date')
        package_data = request.POST.get('Package')
        
        # 2. Directly save the data into your Database Model
        try:
            bookings.objects.create(
                Name=name_data,
                Email=email_data,
                Phone=phone_data,
                Date=date_data,
                Package=package_data
            )
            return redirect('success')

        except Exception as e:
            # 🚨 THIS WILL FORCE THE ERROR TO SHOW ON YOUR SCREEN INSTEAD OF REFRESHING
            return HttpResponse(f"<h1>Database Refused to Save!</h1><p>Error details: {e}</p>")
        
    return render(request, 'booking.html')  

def index (request):
    return render(request, 'index.html')

def success(request):
    return render(request, 'success.html')
