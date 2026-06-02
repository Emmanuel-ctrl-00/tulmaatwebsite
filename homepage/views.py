from django.shortcuts import render, redirect
from .forms import BookingForm

# Create your views here.
def index (request):
    return render(request, 'index.html')

def booking(request):
    return render(request, 'booking.html')

def success(request):
    return render(request, 'success.html')

def book_now(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        
        # 1. TEST: Did the data actually make it to the view?
        print("--- POST DATA RECEIVED: ---", request.POST)
        
        if form.is_valid():
            form.save()
            print("--- SUCCESS: DATA SAVED TO DATABASE! ---")
            return redirect('success.html')
        else:
            # 2. TEST: Why did the form reject the data?
            print("--- FORM VALIDATION FAILED! ERRORS Below: ---")
            print(form.errors) 
            
    else:
        form = BookingForm()
        
    return render(request, 'booking.html', {'form': form})
