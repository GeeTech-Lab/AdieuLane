from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

app_name = 'memorials'

urlpatterns = [
    path("", views.BurialMemoryList.as_view(), name='list'),
    path('create/', views.BurialMemoryCreate.as_view(), name='create'),
    path("<slug:slug>/", views.BurialMemoryDetail.as_view(), name='detail'),
    path('update/<slug:slug>', views.BurialMemoryUpdate.as_view(), name='update'),
    path('delete/<slug:slug>', views.BurialMemoryDelete.as_view(), name='delete'),
    path('gallery_list/', views.GalleryListView.as_view(), name='list_gallery'),
]

htmx_urlpatterns = [
    # path('toggle_donation', views.toggle_accept_donation, name='toggle_donation'),
    path('<slug:slug>/tribute/', views.add_tribute, name='add_tribute'),
    path('<slug:slug>/add_gallery_v2/', views.GalleryAddView.as_view(), name='add_gallery_v2'),
]

urlpatterns += htmx_urlpatterns
