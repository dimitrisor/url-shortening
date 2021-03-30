from http import HTTPStatus
from flask import Blueprint, request, jsonify
from shorty.service.shorty_service import ShortyService
from shorty.dto.shorty_request import ShortyRequest
from shorty.exception.system_exception import SystemException

api = Blueprint('api', __name__)

@api.route('/shortlinks', methods=['POST'])
def create_shortlink():
    try:
        request_data = request.get_json()
        if request_data is None: raise Exception
    except Exception:
        raise SystemException(HTTPStatus.BAD_REQUEST, 'invalid_body')

    data = ShortyRequest(request_data.get('url'), request_data.get('provider'))
    link = ShortyService().get_provider_chain(data.provider).get_shortlink(data.url)

    return jsonify({'url': data.url,'link': link}), HTTPStatus.OK

@api.errorhandler(SystemException)
def handle_exception(e):
    return jsonify({"message": e.get_message()}), e.get_status()

@api.app_errorhandler(404)
def resource_not_found(e):
    return jsonify({"message": "The requested URL was not found on the server"}), e.code