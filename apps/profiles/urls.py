from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    # path('select_currency/', csrf_exempt(views.select_currency), name='select_currency'),
    path('check_phone/', views.check_phone, name='check_phone'),
    path('<slug:slug>/', views.ProfileView.as_view(), name='profile_detail'),
    path('update/<slug:slug>/', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('<slug:slug>/select_country_currency/', csrf_exempt(views.SelectCountryCurrency.as_view()), name="select_country_currency")
]
