from telos.core.base import status_pb2

def get_response(is_ok=True, status_code=status_pb2.StatusCode.STATUS_CODE_OK, params={}):
    response = { 
        'status': {
            'is_ok': is_ok,
            'status_instance': [{
                'status_code': status_code,
                'parameters': {
                    **params,
                }
            }]
        }
    }
    return response
