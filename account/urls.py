from django.urls import path

from .views import registration, sign_in, home


urlpatterns = [
    path('', home, name='home'),
    path('registration/', registration, name='registration'),
    path('login/', sign_in, name='sign_in'),
]
