from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

app_name = 'donations'

urlpatterns = [
    path('<slug:slug>/create_donation_account/', csrf_exempt(views.DonationAccountCreateView.as_view()), name='create_donation_account'),
    path('<slug:slug>/donate/', csrf_exempt(views.add_donation), name='add_donation'),
    path('<slug:slug>/donation_list/', views.list_donations, name='list_donations'),
]
