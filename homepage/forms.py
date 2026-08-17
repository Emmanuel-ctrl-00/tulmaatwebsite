from django import forms
from .models import bookings


class BookingForm(forms.ModelForm):
    class Meta:
        model = bookings
        fields = ['Name', 'Email', 'Phone', 'Date', 'Package']
        widgets = {
            'Name': forms.TextInput(attrs={
                'placeholder': 'Emmanuel Mutai', 'autocomplete': 'name',
            }),
            'Email': forms.EmailInput(attrs={
                'placeholder': 'emmanuel@gmail.com', 'autocomplete': 'email',
            }),
            'Phone': forms.TextInput(attrs={
                'placeholder': '+254712345678', 'autocomplete': 'tel', 'inputmode': 'tel',
            }),
            'Date': forms.DateInput(attrs={'type': 'date'}),
            'Package': forms.Select(),
        }

    def clean_Phone(self):
        phone = self.cleaned_data['Phone'].strip()
        digits = phone.replace('+', '').replace(' ', '')
        if not digits.isdigit() or len(digits) < 9:
            raise forms.ValidationError('Enter a valid phone number, e.g. +254712345678.')
        return phone
