from model_manager.utils.base_utils import get_response
from model_manager.utils.model_store_utils import read_model
from model_manager.utils.services.adapter.adapter import Adapter
from model_manager.proto import model_schema_pb2
from google.protobuf import text_format, json_format
import os, json
import numpy as np
import tempfile

def get_model_config(model_url, model_format):
    model_file = model_url.split('/')[-1].split('.')[0]
    model_file = f"{model_file}.{model_format}"
    return model_file

class ServicerHandler:
    def handle_import_model(request):
        print('request', request)
        model_token, model_url = request.model_token, request.import_location.aws_s3.bucket
        # model_schema = read_model(model_token)
        model_file = get_model_config(model_url, model_format='textproto')
        adapter = Adapter()
        print('model_url, model_file \n', model_url, model_file, '\n')
        p, h, m = adapter.import_model(model_url)
        # print('p , h , m \n', p, '\n', '\n', h, '\n', m, '\n')
        p["coef_"] = json.dumps(p["coef_"].tolist())
        model_data = model_schema_pb2.ModelSchema(hyperparameters=h, parameters=p, model_details=m)
        model_textproto_data = text_format.MessageToString(model_data)

        fh = open(model_file, 'w')
        try:
            fh.write(model_textproto_data)
            fh.close()
        finally:
            adapter.upload_to_url(model_file)
            os.remove(model_file)
        response = get_response(params={})
        return response

    def handle_export_model(request):
        model_token, model_url, export_format = request.model_token, request.export_location.aws_s3.bucket, 'joblib'
        model_file = get_model_config(model_url, model_format=export_format)
        adapter = Adapter()
        model_url_blob = adapter.download_blob_from_url(model_url)
        with open(model_url_blob, 'r') as f:
            model_data = text_format.Parse(f.read(), model_schema_pb2.ModelSchema())
        h, p, m = model_data.hyperparameters, model_data.parameters, model_data.model_details
        h, p, m = json_format.MessageToDict(h, preserving_proto_field_name=True), \
            json_format.MessageToDict(p, preserving_proto_field_name=True), json_format.MessageToDict(m, preserving_proto_field_name=True)
        p["coef_"] = np.array(json.loads(p["coef_"]))

        model_name, output_framework = model_file.split('.')[0], m['Framework']
        print('p , h , m \n', p, '\n', '\n', h, '\n', m, '\n', output_framework, '\n', model_url, '\n', model_name)
        adapter.export_model(h, p, m, output_framework=output_framework, output_format=export_format, model_name=model_name)
        response = get_response(params={})
        return response

    def handle_deploy_model(request):
        model_name = request.model_name
        response = get_response(params={ 'model_name': model_name })
        return response
