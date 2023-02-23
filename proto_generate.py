# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.
from csv import DictReader
import os

def _get_proto_content():
    PROTO_CONTENT = '''
syntax = "proto3";

package telos.cortex.model_schema;

option go_package = "telos/cortex/model_schema";
option java_package = "com.telos.cortex.model_schema";
option java_multiple_files = true;

message ModelSchema {{
	HyperParameter hyperparameters = 1;
	string parameters = 2;
	string attributes = 3;
	string model_details = 4;
}}

message StrVector {{
  repeated string element = 1;
}}

message HyperParameter {{
{hyperparameter_schema}
}}
'''
    return PROTO_CONTENT

ROOT_DIR = '/Users/pramod19.kumar/Documents/statusneo/model-manager'
HYPER_PARAMETER_CSV_PATH = f'{ROOT_DIR}/vault/core/cortex/schema/classification/binary/logistic_regression/hyperparameter/hyperparameter.csv'
proto_file_fath = f'{ROOT_DIR}/model_manager/utils/services/Adapter/'
with open(HYPER_PARAMETER_CSV_PATH, 'r') as hyperparameter_obj:
    hyperparameter_fields, hyperparameter_schema, row_count = DictReader(hyperparameter_obj), '', 1
    for field in hyperparameter_fields:
        hyperparameter_schema += f"\t{'optional' if field['required']=='False' else ''} {field['type']} {field['hyperparameter_name']} = {row_count}; \n"
        row_count += 1
    proto_content = _get_proto_content()
    proto_content = proto_content.format(hyperparameter_schema=hyperparameter_schema)
    proto_file = open(os.path.join(proto_file_fath, 'model_schema.proto'), 'w+')
    proto_file.write(proto_content)
    print('proto_content', proto_content)
