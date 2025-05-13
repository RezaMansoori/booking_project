from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_redirect, name='home_redirect'),
    path('auth/', views.auth_view, name='auth'),
    path('bookings/', views.booking_list, name='booking_list'),
    path('booking/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('hotels/', views.hotel_list, name='hotel_list'),
    path('flights/', views.flight_list, name='flight_list'),
    path('tours/', views.tour_list, name='tour_list'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('add_room/<int:hotel_id>/', views.add_room, name='add_room'),
    path('edit_room/<int:room_id>/', views.edit_room, name='edit_room'),
    path('delete_room/<int:room_id>/', views.delete_room, name='delete_room'),
    path('add_flight/<int:airline_id>/', views.add_flight, name='add_flight'),
    path('edit_flight/<int:flight_id>/', views.edit_flight, name='edit_flight'),
    path('delete_flight/<int:flight_id>/', views.delete_flight, name='delete_flight'),
    path('add_tour/<int:tour>/', views.add_tour, name='add_tour'),
    path('edit_tour/<int:tour>/', views.edit_tour, name='edit_tour'),
    path('delete_tour/<int:tour>/', views.delete_tour, name='delete_tour'),
    path('reserve/<str:item_type>/<int:item_id>/', views.reserve_item, name='reserve_item'),
    path('cancel_reservation/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),
]