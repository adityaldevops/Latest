import os

class AppConfig:
    APP_SERVICE_PORT = os.getenv("APP_SERVICE_PORT", 50051)
    MODEL_STORE_SERVICE_PORT = os.getenv("MODEL_STORE_SERVICE_PORT", 4770)
