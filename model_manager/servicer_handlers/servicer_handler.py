from model_manager.utils.base_utils import get_response
from model_manager.utils.services.Adapter.adapter import Adapter


class ServicerHandler:
    def handle_import_model(request):
        model_name = request.model_name
        adapter = Adapter()
        p , a , h , m = adapter.import_model(model_name)
        print('p , a , h , m \n', p , a , h , m)
        response = get_response(params={ 'model_name': model_name })
        return response

    def handle_export_model(request):
        model_name = request.model_name
        adapter = Adapter()
        p , a , h , m = adapter.import_model(model_name)
        print('p , a , h , m \n', p , a , h , m)
        ROOT_DIR = '/Users/pramod19.kumar/Documents/statusneo/model-manager'
        MODEL_PATH = f'{ROOT_DIR}/model_manager/store/export_models/'
        model_name_export, output_format = 'Ridge_Regression_Exported', 'pickle'
        adapter.export_model(h, p, a, m, output_format=output_format, export_path=MODEL_PATH, model_name=model_name_export)
        response = get_response(params={ 'model_name': model_name })
        return response

    def handle_deploy_model(request):
        model_name = request.model_name
        response = get_response(params={ 'model_name': model_name })
        return response
