import grpc
from config.config import AppConfig
from telos.cortex.store.crud.model import service_pb2_grpc as model_svc_pb2_grpc


def connect_store(func):
    def wrapper(*args, **kwargs):
        with grpc.insecure_channel(f'localhost:{AppConfig.MODEL_STORE_SERVICE_PORT}') as channel:
            stub = model_svc_pb2_grpc.ModelStoreServiceStub(channel)
            kwargs['stub'] = stub
            return func(*args, **kwargs)
    return wrapper
