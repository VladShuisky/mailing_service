from vk_api.exceptions import ApiError


res_msg = {
    1: 'request_sended',
    2: 'request_already_approved'
}

detail = {
    'response_code': None,
    'response_msg': None
}

def response_detail(response):
    if isinstance(response, ApiError):
        return {
            'response_code': response.error.get('error_code'),
            'response_status': 'error',
            'response_msg': response.error.get('error_msg')
        }
    elif isinstance(response, int):
        return {
            'response_code': response,
            'response_status': res_msg.get(response, None),
            'response_msg': None
        }
    elif isinstance(response, Exception):
        return {
            'response_code': None,
            'response_status': type(response),
            'response_msg': str(response)
        }
    return None