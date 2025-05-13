from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    is_customer = models.BooleanField(default=True)
    is_hotel_manager = models.BooleanField(default=False)
    is_airline_manager = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_tour_operator = models.BooleanField(default=False)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    def role(self):
        if self.is_customer:
            return "Customer"
        elif self.is_hotel_manager:
            return "Hotel Manager"
        elif self.is_airline_manager:
            return "Airline Manager"
        elif self.is_staff:
            return "Staff"
        elif self.is_tour_operator:
            return "Tour Operator"
        else:
            return "Unknown"
    def __str__(self):
        return self.username


class Hotel(models.Model):
    name = models.CharField(max_length=200)
    location_city = models.CharField(max_length=100)
    location_address = models.TextField()
    description = models.TextField(blank=True)
    star_rating = models.PositiveSmallIntegerField(choices=[(i, f"{i} Star{'s' if i > 1 else ''}") for i in range(1, 6)])
    contact_email = models.EmailField(blank=True)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name="managed_hotels")

    def __str__(self):
        return f"{self.name} ({self.location_city})"
    
class Amenity(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon_class = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., 'fas fa-wifi'") # For Font Awesome or similar

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Amenities"
        
class RoomType(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="e.g., Single, Double, Suite, Deluxe King")
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="rooms")
    room_type = models.ForeignKey(RoomType, on_delete=models.SET_NULL, null=True)
    room_number = models.CharField(max_length=10, help_text="e.g., '101', 'A-203'")
    capacity = models.IntegerField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    amenities = models.ManyToManyField(Amenity, blank=True, related_name='rooms')
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.hotel.name} - Room {self.room_number}"

    class Meta:
        unique_together = ('hotel', 'room_number')
        
class Airline(models.Model):
    name = models.CharField(max_length=100)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name="managed_airlines")
    def __str__(self):
        return self.name


class Flight(models.Model):
    flight_number = models.CharField(max_length=20, unique=True)
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)
    seat_count = models.IntegerField()
    available_seats = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.flight_number

class Tour(models.Model):
    name = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='tours')
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='tours')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    guide = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="tours_guided")
    capacity = models.IntegerField()
    available_slots = models.IntegerField()

    def __str__(self):
        return f"{self.name} - {self.destination}"

class Reservation(models.Model):
    RESERVATION_TYPE_CHOICES = [
        ("HOTEL", "Hotel"),
        ("FLIGHT", "Flight"),
        ("TOUR", "Tour"),
    ]

    PAYMENT_STATUS_CHOICES = [
        ("PAID", "Paid"),
        ("UNPAID", "Unpaid"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reservations")
    reservation_type = models.CharField(max_length=10, choices=RESERVATION_TYPE_CHOICES)
    tour = models.ForeignKey(Tour, null=True, blank=True, on_delete=models.SET_NULL)
    room = models.ForeignKey(Room, null=True, blank=True, on_delete=models.SET_NULL)
    flight = models.ForeignKey(Flight, null=True, blank=True, on_delete=models.SET_NULL)
    seat_number = models.CharField(max_length=10, blank=True, null=True)
    reservation_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES)

    def __str__(self):
        return f"Reservation {self.id} - {self.user.username}"


class Payment(models.Model):
    PAYMENT_METHODS = [
        ("CREDIT_CARD", "Credit Card"),
        ("PAYPAL", "PayPal"),
    ]

    PAYMENT_STATUS = [
        ("PAID", "Paid"),
        ("UNPAID", "Unpaid"),
    ]

    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS)

    def __str__(self):
        return f"Payment for Reservation {self.reservation.id}"


class Review(models.Model):
    REVIEW_TYPE_CHOICES = [
        ("HOTEL", "Hotel"),
        ("FLIGHT", "Flight"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review_type = models.CharField(max_length=10, choices=REVIEW_TYPE_CHOICES)
    hotel = models.ForeignKey(Hotel, null=True, blank=True, on_delete=models.SET_NULL)
    flight = models.ForeignKey(Flight, null=True, blank=True, on_delete=models.SET_NULL)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} - {self.review_type}"

