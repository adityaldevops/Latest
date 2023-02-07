import os

class AppConfig:
    APP_SERVICE_PORT = os.getenv("APP_SERVICE_PORT", 50051)
