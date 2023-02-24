from model_manager.utils.base_utils import get_response
from model_manager.utils.services.adapter.adapter import Adapter
from model_manager.proto import  model_schema_pb2
from google.protobuf import text_format

class ServicerHandler:
    def handle_import_model(request):
        model_name = request.model_name
        adapter = Adapter()
        p, h, m = adapter.import_model(model_name)
        print('p , a , h , m \n', p, '\n', '\n', h, '\n', m, '\n')
        ROOT_DIR = '/Users/pramod19.kumar/Documents/statusneo/model-manager'
        MODEL_PATH = f'{ROOT_DIR}/model_manager/store/import_models/proto_model.textproto'
        model_data = model_schema_pb2.ModelSchema(hyperparameters=h) 
        with open(MODEL_PATH, 'w') as f:
            text_format.PrintMessage(model_data, f)
        with open(MODEL_PATH, 'r') as f:
            model_data_pb = text_format.Parse(f.read(), model_schema_pb2.ModelSchema())
            model_data_pb = text_format.MessageToString(model_data_pb)
        print('model_data_pb \n', model_data_pb)
        print('model_data \n', model_data)
        response = get_response(params={ 'model_name': model_name })
        return response

    def handle_export_model(request):
        model_name = request.model_name
        adapter = Adapter()
        p , a , h , m = adapter.import_model(model_name)
        print('p , a , h , m \n', p , a , h , m)
        ROOT_DIR = '/Users/pramod19.kumar/Documents/statusneo/model-manager'
        MODEL_PATH = f'{ROOT_DIR}/model_manager/store/export_models/'
        model_name_to_export = model_name.split('models/')[1]
        model_name_export, output_format = f'Exported_{model_name_to_export}', 'pickle'
        adapter.export_model(h, p, a, m, output_format=output_format, export_path=MODEL_PATH, model_name=model_name_export)
        response = get_response(params={ 'model_name': model_name })
        return response

    def handle_deploy_model(request):
        model_name = request.model_name
        response = get_response(params={ 'model_name': model_name })
        return response
