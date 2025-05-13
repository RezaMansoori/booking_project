from django.contrib import admin
from .models import User, Hotel, Room, Flight, Airline, Reservation, Payment, Review, Amenity, RoomType

admin.site.register(User)
admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(Flight)
admin.site.register(Airline)
admin.site.register(Reservation)
admin.site.register(Payment)
admin.site.register(Review)
admin.site.register(Amenity)
admin.site.register(RoomType)