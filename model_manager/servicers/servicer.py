from telos.cortex.model_manager import service_pb2_grpc, service_pb2
from model_manager.servicer_handlers.servicer_handler import ServicerHandler

class CortexModelManagerServicer(service_pb2_grpc.CortexModelManagerServicer):

  def ImportModelInstance(self, request, context):
    data = ServicerHandler.handle_import_model(request)
    response = service_pb2.ImportModelInstanceResponse(**data)
    return response

  def ExportModelInstance(self, request, context):
    data = ServicerHandler.handle_export_model(request)
    response = service_pb2.ExportModelInstanceResponse(**data)
    return response

  def DeployModelInstance(self, request, context):
    data = ServicerHandler.handle_deploy_model(request)
    response = service_pb2.DeployModelInstanceResponse(**data)
    return response
