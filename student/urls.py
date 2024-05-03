from django.urls import path

from .views import track_student, BookingCreateAPIView

urlpatterns = [
    path('<int:ttj_id>/<int:student_id>/', track_student, name='track-student'),
    path('bookings/create/', BookingCreateAPIView.as_view(), name='booking-create'),
]

    