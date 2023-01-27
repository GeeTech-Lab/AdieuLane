from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('accounts/', include(('apps.accounts.urls', 'apps.accounts'), namespace='accounts')),
    path('api/accounts/', include(('apps.accounts.api.urls', 'apps.accounts'), namespace='api_accounts')),
    path('profiles/', include(('apps.profiles.urls', 'apps.profiles'), namespace='profiles')),
    path('api/profiles/', include(('apps.profiles.api.urls', 'apps.profiles'), namespace='profiles_api')),
    path('memorials/', include(('apps.memorials.urls', 'apps.memorials'), namespace='memorials')),
    path('donations/', include(('apps.donations.urls', 'apps.donations'), namespace='donations')),
    path('wallets/', include(('apps.wallets.urls', 'apps.wallets'), namespace='wallets')),
    path('notifications/', include(('apps.notifications.urls', 'apps.notifications'), namespace='notifications')),
    path('currencies/', include('currencies.urls')),
    # path("api/v1/auth/", include("djoser.urls")),
    # path("api/v1/auth/", include("djoser.urls.jwt")),
    # path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    # path('jet/', include('jet.urls', 'jet')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='404.html'))]

admin.site.site_header = "AdieuLane Admin"
admin.site.site_title = "AdieuLane Admin Portal"
admin.site.index_title = "Welcome to the AdieuLane administration"
