from flask import jsonify

def api_response(status_code, message, data=None):
    response = {
        'status': status_code,
        'message': message
    }
    if data is not None:
        response['data'] = data
    return jsonify(response), status_code
