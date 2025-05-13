from django import forms
from django.forms import inlineformset_factory
from .models import Hotel, Room, Flight, Airline, Tour


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = [
            "room_number",
            "room_type",
            "capacity",
            "price_per_night",
            "is_available",
        ]
        widgets = {
            "room_number": forms.TextInput(attrs={"class": "form-control"}),
            "room_type": forms.Select(attrs={"class": "form-select"}),
            "capacity": forms.NumberInput(attrs={"class": "form-control"}),
            "price_per_night": forms.NumberInput(attrs={"class": "form-control"}),
            "is_available": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


RoomFormSet = inlineformset_factory(
    Hotel, Room, form=RoomForm, extra=1, can_delete=True
)


class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = [
            "flight_number",
            "origin",
            "destination",
            "departure_time",
            "arrival_time",
            "airline",
            "seat_count",
            "available_seats",
            "price",
        ]
        widgets = {
            "departure_time": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"}
            ),
            "arrival_time": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"}
            ),
        }


FlightFormSet = inlineformset_factory(
    Airline, Flight, form=FlightForm, extra=1, can_delete=True
)
