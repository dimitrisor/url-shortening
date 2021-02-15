from http import HTTPStatus
from flask import Blueprint, request, jsonify
from shorty.service.shorty_service import ShortyService as service
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

    data = ShortyRequest(request_data.get('cls'), request_data.get('provider'))

    provider_chain = service.get_provider_chain(data.provider)
    link = provider_chain.get_shortlink(data.cls)

    return jsonify({'cls': data.cls,'link': link}), HTTPStatus.OK

@api.errorhandler(SystemException)
def handle_exception(e):
    return jsonify({"message": e.get_message()}), e.get_status()