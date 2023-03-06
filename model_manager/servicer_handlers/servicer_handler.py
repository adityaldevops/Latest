from model_manager.utils.base_utils import get_response
from model_manager.utils.model_store_utils import read_model
from model_manager.utils.services.adapter.adapter import Adapter
from model_manager.proto import model_schema_pb2
from google.protobuf import text_format, json_format
import os, json
import numpy as np
# import tempfile

def get_model_config(action_type=None, model_file='LogisticRegressionModel.pkl', model_format='textproto'):
    # model_base_url, model_folder = f'/Users/pramod19.kumar/Documents/statusneo/model-manager/model_manager/store', 'models'
    model_base_url, model_folder = f'https://cortexstorageaccount3597.blob.core.windows.net/content', 'models'
    if (action_type):
        model_store_folder = f'{action_type}_{model_folder}'
    model_store_file = f"{model_file.split('.')[0]}.{model_format}"
    # store_location = f'{model_base_url}/{model_store_folder}/{model_store_file}'
    store_location = f'{model_base_url}/{model_store_file}'
    return store_location

class ServicerHandler:
    def handle_import_model(request):
        print('request', request)
        model_token, model_url = request.model_token, request.import_location.aws_s3.bucket
        # model_schema = read_model(model_token)
        store_location = get_model_config(action_type='import')
        adapter = Adapter()
        print('model_url, store_location \n', model_url, store_location)
        p, h, m = adapter.import_model(model_url)
        print('p , h , m \n', p, '\n', '\n', h, '\n', m, '\n')
        p["coef_"] = json.dumps(p["coef_"].tolist())
        model_data = model_schema_pb2.ModelSchema(hyperparameters=h, parameters=p, model_details=m)

        with open(store_location, 'w') as f:
            model_textproto_data = text_format.PrintMessage(model_data, f)
            print('model_textproto_data', '\n', model_textproto_data)
        adapter.upload_to_url('https://cortexstorageaccount3597.blob.core.windows.net/content', store_location)
        with open(store_location, 'r') as f:
            model_data_pb = text_format.Parse(f.read(), model_schema_pb2.ModelSchema())
        print('model_data_pb \n', model_data_pb)
        response = get_response(params={})
        return response

    def handle_export_model(request):
        model_token, model_url, export_format = request.model_token, request.export_location.aws_s3.bucket, 'joblib'
        store_location = get_model_config(action_type='export', model_format=export_format)
        with open(model_url, 'r') as f:
            model_data = text_format.Parse(f.read(), model_schema_pb2.ModelSchema())
        h, p, m = model_data.hyperparameters, model_data.parameters, model_data.model_details
        h, p, m = json_format.MessageToDict(h, preserving_proto_field_name=True), \
            json_format.MessageToDict(p, preserving_proto_field_name=True), json_format.MessageToDict(m, preserving_proto_field_name=True)
        p["coef_"] = np.array(json.loads(p["coef_"]))

        model_name, output_framework = store_location.split('/')[-1].split('.')[0], m['Framework']
        export_path = store_location.split(model_name)[0]
        print('p , h , m \n', p, '\n', '\n', h, '\n', m, '\n', output_framework, '\n', model_url, '\n', export_path, '\n', model_name)
        adapter = Adapter()
        adapter.export_model(h, p, m, output_framework=output_framework, output_format=export_format, export_path=export_path, model_name=model_name)
        response = get_response(params={})
        return response

    def handle_deploy_model(request):
        model_name = request.model_name
        response = get_response(params={ 'model_name': model_name })
        return response
