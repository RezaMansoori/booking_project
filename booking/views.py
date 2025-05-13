from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.db.models import Min
from .models import User, Hotel, Room, Airline, Flight, Reservation, Tour
from .forms import RoomForm, FlightForm


# pages views
def home_redirect(request):
    return redirect("auth")


def auth_view(request):
    if request.session.get("username"):
        return redirect("profile")

    error = ""
    if request.method == "POST":
        action = request.POST.get("action")
        username = request.POST.get("username")
        password = request.POST.get("password")

        if action == "register":
            email = request.POST.get("email")
            if User.objects.filter(username=username).exists():
                error = "this username already exists."
            elif User.objects.filter(email=email).exists():
                error = "This email is already registered."
            else:
                user = User(username=username, email=email, password=password)
                user.save()
                request.session["username"] = username
                return redirect("profile")

        elif action == "login":
            try:
                user = User.objects.get(username=username, password=password)
                request.session["username"] = username
                next_url = request.GET.get("next")
                if next_url:
                    return redirect(next_url)
                return redirect("profile")
            except User.DoesNotExist:
                error = "Invalid username or password."

    return render(request, "auth.html", {"error": error})


def logout_view(request):
    request.session.flush()
    return redirect("auth")


def booking_list(request):
    if "username" not in request.session:
        return redirect("auth")

    user = User.objects.get(username=request.session["username"])

    if user.is_hotel_manager:
        hotels = Hotel.objects.filter(manager=user)
        rooms = Room.objects.filter(hotel__in=hotels)
        return render(
            request,
            "booking_list.html",
            {"user": user, "rooms": rooms, "hotels": hotels},
        )
    elif user.is_airline_manager:
        airlines = Airline.objects.filter(manager=user)
        flights = Flight.objects.filter(airline__in=airlines)
        return render(
            request,
            "booking_list.html",
            {"user": user, "flights": flights, "airlines": airlines},
        )
    elif user.is_tour_operator:
        tours = Tour.objects.filter(operator=user)
        return render(request, "booking_list.html", {"user": user, "tours": tours})
    else:
        bookings = Reservation.objects.filter(user=user)
        return render(request, "booking_list.html", {"user": user, "bookings": bookings})


def booking_detail(request, booking_id):
    if "username" not in request.session:
        return redirect(f"/login/?next={request.path}")

    booking = Reservation.objects.get(id=booking_id)
    return render(request, "booking_detail.html", {"booking": booking})


def hotel_list(request):
    hotels = Hotel.objects.annotate(min_price=Min("rooms__price_per_night"))
    user_role = None
    if request.session.get("username"):
        user = User.objects.get(username=request.session["username"])
        user_role = user.role
    return render(request, "hotel_list.html", {"hotels": hotels})


def flight_list(request):
    flights = Flight.objects.all()
    user_role = None
    if request.session.get("username"):
        user = User.objects.get(username=request.session["username"])
        user_role = user.role
    return render(
        request, "flight_list.html", {"flights": flights, "user_role": user_role}
    )


def tour_list(request):
    tours = Tour.objects.all()
    return render(request, 'tour_list.html', {'tours': tours})

def profile_view(request):
    username = request.session.get("username")
    if not username:
        return redirect("auth")
    user = User.objects.get(username=username)
    return render(request, "profile.html", {"user": user})


# CRUD operations


# CRUD operations for Hotel
def add_room(request, hotel_id):
    if "username" not in request.session:
        return redirect("auth")

    user = User.objects.get(username=request.session["username"])
    hotel = get_object_or_404(Hotel, id=hotel_id)

    if hotel.manager != user:
        return HttpResponseForbidden("You are not allowed to add rooms to this hotel.")

    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.hotel = hotel
            room.save()
            return redirect("booking_list")
    else:
        form = RoomForm()

    return render(request, "add_room.html", {"form": form, "hotel": hotel})


def edit_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect("booking_list")
    else:
        form = RoomForm(instance=room)

    return render(request, "edit_room.html", {"form": form, "room": room})


def delete_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    hotel_id = room.hotel.id
    room.delete()
    return redirect("booking_list")


# CRUD operations for Flight
def add_flight(request, airline_id):
    if "username" not in request.session:
        return redirect("auth")

    user = User.objects.get(username=request.session["username"])
    airline = get_object_or_404(Airline, id=airline_id)

    if airline.manager != user:
        return HttpResponseForbidden("You are not allowed to add flights to this airline.")
    
    if request.method == "POST":
        form = FlightForm(request.POST)
        if form.is_valid():
            flight = form.save(commit=False)
            flight.airline = airline
            flight.save()
            return redirect("booking_list")
    else:
        form = FlightForm()

    return render(request, "add_flight.html", {"form": form, "airline": airline})

def edit_flight(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)

    if request.method == "POST":
        form = FlightForm(request.POST, instance=flight)
        if form.is_valid():
            form.save()
            return redirect("booking_list")
    else:
        form = FlightForm(instance=flight)

    return render(request, "edit_flight.html", {"form": form, "flight": flight})


def delete_flight(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    airline_id = flight.airline.id
    flight.delete()
    return redirect("booking_list")


# CRUD operations for Tour
def add_tour(request, tour_id):
    if "username" not in request.session:
        return redirect("auth")

    user = User.objects.get(username=request.session["username"])
    tour = get_object_or_404(Tour, id=tour_id)

    if tour.guide != user:
        return HttpResponseForbidden("You are not allowed to add tour.")
    
    if request.method == "POST":
        form = FlightForm(request.POST)
        if form.is_valid():
            flight = form.save(commit=False)
            flight.tour = tour
            flight.save()
            return redirect("booking_list")
    else:
        form = FlightForm()

    return render(request, "add_tour.html", {"form": form, "tour": tour})


def edit_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)

    if request.method == "POST":
        form = FlightForm(request.POST, instance=tour)
        if form.is_valid():
            form.save()
            return redirect("booking_list")
    else:
        form = FlightForm(instance=tour)

    return render(request, "edit_tour.html", {"form": form, "tour": tour})


def delete_tour(request, tour_id):
    tour = get_object_or_404(Tour, id=tour_id)
    tour.delete()
    return redirect("booking_list")


# CRUD operations for Reservation
def reserve_item(request, item_type, item_id):
    if "username" not in request.session:
        return redirect("auth")

    user = User.objects.get(username=request.session["username"])
    reservation = Reservation(user=user)

    if item_type == "room":
        reservation.room = get_object_or_404(Room, id=item_id)
        reservation.reservation_type = "HOTEL"
        reservation.payment_status = "PAID"
    elif item_type == "flight":
        reservation.flight = get_object_or_404(Flight, id=item_id)
        reservation.reservation_type = "FLIGHT"
        reservation.payment_status = "PAID"
    elif item_type == "tour":
        reservation.tour = get_object_or_404(Tour, id=item_id)
        reservation.reservation_type = "TOUR"
        reservation.payment_status = "PAID"
    else:
        return HttpResponseForbidden("Invalid item type")

    reservation.save()
    return redirect("booking_list")

def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)

    if reservation.user.username != request.session.get("username"):
        return HttpResponseForbidden("You can't cancel this reservation.")

    reservation.delete()
    return redirect("booking_list")