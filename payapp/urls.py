
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('make-payment/', views.make_payment, name='make_payment'),
    path('request-payment/', views.request_payment, name='request_payment'),
    path('respond-request/<int:transaction_id>/<str:action>/', 
         views.respond_to_request, name='respond_to_request'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]