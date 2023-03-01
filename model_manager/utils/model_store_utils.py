from model_manager.utils.wrappers.connection_handler import connect_store             
from telos.cortex.store.crud.model import service_pb2 as model_svc_pb2


@connect_store
def read_model(model_token, **kwargs):
    stub = kwargs['stub']
    request_data = [ model_token ]
    response = stub.ReadModel(model_svc_pb2.ReadModelRequest(**request_data))
    print("import model response: ", response.status, model_token, stub)
    