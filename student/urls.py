from django.urls import path

from .views import track_student

urlpatterns = [
    path('<int:ttj_id>/<int:student_id>/', track_student, name='track-student'),
]
