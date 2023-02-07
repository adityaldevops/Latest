from telos.cortex.model_manager import service_pb2_grpc, service_pb2
from model_manager.servicer_handlers.servicer_handler import ServicerHandler

class CortexModelManagerServicer(service_pb2_grpc.CortexModelManagerServicer):

  def ImportModel(self, request, context):
    data = ServicerHandler.handle_import_model(request)
    response = service_pb2.ImportModelResponse(**data)
    return response

  def ExportModel(self, request, context):
    data = ServicerHandler.handle_export_model(request)
    response = service_pb2.ExportModelResponse(**data)
    return response

  def DeployModel(self, request, context):
    data = ServicerHandler.handle_deploy_model(request)
    response = service_pb2.DeployModelResponse(**data)
    return response
