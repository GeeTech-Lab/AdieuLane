import os
from adieulane.settings import DEBUG

if DEBUG:
    # test key
    FLUTTERWAVE_SECRET_KEY = os.environ.get('TEST_FLUTTERWAVE_SECRET_KEY')
    FLUTTERWAVE_PUBLIC_KEY = os.environ.get('TEST_FLUTTERWAVE_PUBLIC_KEY')
    FLUTTERWAVE_ENCRYPTION_KEY = os.environ.get('TEST_FLUTTERWAVE_ENCRYPTION_KEY')
else:
    # live key
    FLUTTERWAVE_SECRET_KEY = os.environ.get('FLUTTERWAVE_SECRET_KEY')
    FLUTTERWAVE_PUBLIC_KEY = os.environ.get('FLUTTERWAVE_PUBLIC_KEY')
    FLUTTERWAVE_ENCRYPTION_KEY = os.environ.get('FLUTTERWAVE_ENCRYPTION_KEY')
