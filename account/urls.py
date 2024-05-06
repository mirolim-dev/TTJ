from django.urls import path

from .views import registration, sign_in, home, get_faculties


urlpatterns = [
    path('', home, name='home'),
    path('registration/', registration, name='registration'),
    path('login/', sign_in, name='sign_in'),

    path('registration/get_faculties/', get_faculties, name='get_faculties'),
]
