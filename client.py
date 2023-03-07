import grpc
from config.config import AppConfig
from telos.cortex.model_manager import service_pb2_grpc as model_manager_svc_pb2_grpc, service_pb2 as model_manager_svc_pb2
from telos.core.base import enums_pb2
from telos.cortex.model.instance import artifact_pb2

MODEL_PATH = "https://cortexstorageaccount3597.blob.core.windows.net/content"

def get_token():
    import ctypes, random
    token = ctypes.c_uint32(random.randint(100000, 1000000) * random.randint(100000, 1000000)).value
    return token

def get_request_data(action_type):
    model_url = f'{MODEL_PATH}/LogisticRegressionModel.pkl'
    request_data = {
        'model_token': {
            'vertical': 'vertical',
            'type': enums_pb2.TokenType.TELOS_CORTEX_MODEL_TOKEN,
            'id': {
                'key': '/telecom/quantity/rsrp',
                'u32': get_token()
            },
            'model': {
                'model': {
                    'name': {
                        'path': ["telecom","quantity","rsrp"]
                    }
                }
            }
        },
        f'{action_type}_location': {
            'type': artifact_pb2.ARTIFACT_STORE_TYPE_AWS_S3,
            'aws_s3': {
                'bucket': model_url
            }
        }
    }
    return request_data
    

def run():
    with grpc.insecure_channel(f'localhost:{AppConfig.APP_SERVICE_PORT}') as channel:
        stub = model_manager_svc_pb2_grpc.CortexModelManagerStub(channel)

        request_data = get_request_data('import')
        response = stub.ImportModelInstance(model_manager_svc_pb2.ImportModelInstanceRequest(**request_data))
        print("import model response: ", response.status)

        # request_data = get_request_data('export')
        # response = stub.ExportModelInstance(model_manager_svc_pb2.ExportModelInstanceRequest(**request_data))
        # print("export model response: ", response.status)

        # response = stub.DeployModelInstance(model_manager_svc_pb2.DeployModelInstanceRequest(model_name=model_name))
        # print("deploy model response: ", response.status)

if __name__ == '__main__':
    run()
