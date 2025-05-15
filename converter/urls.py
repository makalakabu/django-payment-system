# converter/urls.py
from django.urls import path
from . import views

app_name = 'converter'

urlpatterns = [
    path(
        '<str:currency1>/<str:currency2>/<str:amount_of_currency1>/',
        views.convert_currency,
        name='convert_currency'
    ),
]
