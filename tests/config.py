import os

BASE_URL = os.getenv("BASE_URL") or "https://goatflow-demo.gibbsoft.com"
#15000ms = 15 detik
DEFAULT_TIMEOUT_MS = 15000

CUSTOMER_LOGIN = os.getenv("CUSTOMER_LOGIN") or "emma.scott.3012"
CUSTOMER_PASSWORD = os.getenv("CUSTOMER_PASSWORD") or "Emma"