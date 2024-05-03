from django.urls import path

from .views import registration, sign_in


urlpatterns = [
    path('', registration, name='registration'),
    path('login/', sign_in, name='sign_in'),
]
