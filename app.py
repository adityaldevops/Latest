from concurrent import futures
import grpc
from config.config import AppConfig
from telos.cortex.model_manager import service_pb2_grpc
from model_manager.servicers.servicer import CortexModelManagerServicer


def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  service_pb2_grpc.add_CortexModelManagerServicer_to_server(
      CortexModelManagerServicer(), server)
  server.add_insecure_port(f'[::]:{AppConfig.APP_SERVICE_PORT}')
  server.start()
  server.wait_for_termination()


if __name__ == '__main__':
    serve()
