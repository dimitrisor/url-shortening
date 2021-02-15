from http import HTTPStatus
from flask import Blueprint, request, jsonify
from shorty.service.shorty_service import ShortyService as service
from shorty.validation.request_validator import RequestValidator
from shorty.dto.shorty_request import ShortyRequest
from shorty.exception.system_exception import SystemException

api = Blueprint('api', __name__)

@api.route('/shortlinks', methods=['POST'])
def create_shortlink():
    RequestValidator.validate(request)
    data = ShortyRequest(request.get_json().get('cls'), request.get_json().get('provider'))

    provider_chain = service.get_provider_chain(data.provider)
    link = provider_chain.get_shortlink(data.cls)

    return jsonify({'cls': data.cls,'link': link}), HTTPStatus.OK

@api.errorhandler(SystemException)
def handle_exception(e):
    return jsonify({"message": e.get_message()}), e.get_status()