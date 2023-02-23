import grpc
from config.config import AppConfig
from telos.cortex.model_manager import service_pb2_grpc, service_pb2
import os

ROOT_DIR = os.getcwd() #'/Users/pramod19.kumar/Documents/statusneo/model-manager'
MODEL_PATH = f'{ROOT_DIR}/model_manager/store/models'

def run():
    with grpc.insecure_channel(f'localhost:{AppConfig.APP_SERVICE_PORT}') as channel:
        stub = service_pb2_grpc.CortexModelManagerStub(channel)
        model_name = f'{MODEL_PATH}/LogisticRegressionModel.pkl'
        # model_name = f'{MODEL_PATH}/XGBmodel-numeric.pkl'
        response = stub.ImportModel(service_pb2.ImportModelRequest(model_name=model_name))
        print("import model response: ", response.status)
        # response = stub.ExportModel(service_pb2.ExportModelRequest(model_name=model_name))
        # print("export model response: ", response.status)
        # response = stub.DeployModel(service_pb2.DeployModelRequest(model_name=model_name))
        # print("deploy model response: ", response.status)

if __name__ == '__main__':
    run()
