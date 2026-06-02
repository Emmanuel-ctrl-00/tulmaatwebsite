from django import forms
from .models import bookings  # Import your model (make sure spelling matches exactly)

class BookingForm(forms.ModelForm):
    class Meta:
        model = bookings
        fields = '__all__'
        
        # Option B: If you want to exclude or manually pick fields, you can do this instead:
        # fields = ['guest_name', 'email', 'check_in_date', 'phone_number']