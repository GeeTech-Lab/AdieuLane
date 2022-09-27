import cloudinary
from .base import *


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": 'railway',
        "USER": "postgres",
        "PASSWORD": "C4xMUsQ47QUHbmzxiV5s",
        "HOST": "containers-us-west-36.railway.app",
        "PORT": 5937,
    }
}

EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "geetechlab@gmail.com"
EMAIL_HOST_PASSWORD = "yzgboftjpmhxturj"
EMAIL_PORT = 587
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
# EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = 'support@geetechlab.com'

SITE_NAME = "AdieuLane"


cloudinary.config(
    cloud_name="geetechlab-com",
    api_key="622236724885358",
    api_secret="ZqOEAuVc4BLHp1bMkhxKJ51ye2s",
)
