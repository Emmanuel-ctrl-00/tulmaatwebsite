from django.db import models


class bookings(models.Model):
    Name = models.CharField(max_length=30)
    Email = models.EmailField()
    # CharField, not IntegerField: phone numbers can start with "+" or "0"
    # and are never used arithmetically. An IntegerField would raise an
    # error the moment someone submits "+254712345678".
    Phone = models.CharField(max_length=20)
    Date = models.DateField()
    Package_options = [
        ('1', 'Bed only'),
        ('2', 'Bed and Breakfast'),
        ('3', 'Half board'),
        ('4', 'Full board'),
        ('5', 'Conference room'),
    ]
    Package = models.CharField(max_length=1, choices=Package_options)

    def __str__(self):
        return self.Name

    class Meta:
        verbose_name = "booking"
        verbose_name_plural = "bookings"


class rooms(models.Model):
    Room_number = models.CharField(max_length=10)
    Room_type = models.CharField(max_length=30)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Room {self.Room_number} - {self.Room_type} - {'Available' if self.is_available else 'Not Available'}"

    class Meta:
        verbose_name = "room"
        verbose_name_plural = "rooms"
