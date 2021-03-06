import json
import datetime
import decimal
from django.utils.timezone import is_aware

from django.core.serializers.json import DjangoJSONEncoder
from django.utils import translation
from rest_framework.renderers import BaseRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework.viewsets import GenericViewSet
from rest_framework import exceptions, status
from library.constant.api import SORT_TYPE_TO_ID, ORDER_BY_DESC, SERVICE_MESSAGE
from library.constant.custom_error_messages import CUSTOM_ERROR_MESSAGE
from library.constant.language import LANGUAGES_TO_ID, LANGUAGE_TYPE_VIETNAMESE, ID_TO_LANGUAGES
from library.logs import logger
from library.authorization import service_encode_from_json, get_encode_header, service_decode_to_json, DjangoOverRideJSONEncoder
from library.constant.api import PAGINATOR_PER_PAGE
from library.functions import time_to_string


# Render response cho zlib
class BinaryFileRenderer(BaseRenderer):
    media_type = 'application/octet-stream'
    render_style = 'binary'

    def render(self, data, media_type=None, renderer_context=None):
        return data


class APIView(GenericViewSet):
    CLIENT_ENCODE = True
    renderer_classes = (BinaryFileRenderer,)
    lang = LANGUAGES_TO_ID.get('vi')
    lang_code = 'vi'
    sort = SORT_TYPE_TO_ID['desc']  # default sort via order by desc

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.total_page = None
        self.per_page = PAGINATOR_PER_PAGE
        self.page = 1
        self.total_record = None
        self.is_paging = False

    def initial(self, request, *args, **kwargs):
        self.CLIENT_ENCODE = get_encode_header(request)
        if not self.CLIENT_ENCODE:
            self.renderer_classes = (JSONRenderer,)

    def parse_param_common(self, request):
        self.get_language_header(request)
        translation.activate(self.lang_code)
        self.sort = SORT_TYPE_TO_ID.get(request.GET.get('sort', 'desc'), ORDER_BY_DESC)

    def response(self, data):
        logger('------------Send Data-------------')
        logger(data)
        if self.CLIENT_ENCODE:
            send_data = service_encode_from_json(data)
        else:
            data = json.loads(json.dumps(data, cls=DjangoOverRideJSONEncoder))
            send_data = data
        res = Response(send_data)
        return res

    def response_exception(self, code, mess=None):
        if not mess:
            try:
                _mess = SERVICE_MESSAGE[code]
            except (ValueError, KeyError):
                _mess = ''
        else:
            _mess = mess
        fail = {'success': False, 'code': code, 'detail': _mess}
        raise exceptions.NotAcceptable(fail)

    def validate_exception(self, text=None, code=None):
        fail = {
            'success': False,
            'detail': text,
        }
        if code:
            fail['detail'] = CUSTOM_ERROR_MESSAGE[code][self.lang_code]
            fail['code'] = code

        raise exceptions.ValidationError(fail)

    def response_paging(self, data):
        if not (isinstance(data, list) or isinstance(data, dict)):
            raise exceptions.ParseError('data must be dict or list')

        result = {
            'success': True,
            'detail': data,
            'total_page': self.total_page,
            'total_record': self.total_record,
            'page': self.page,
        }
        if not self.is_paging:
            if isinstance(data, list):
                result['total_record'] = len(data)
        return result

    def response_success(self, data):
        result = {
            'success': True,
            'detail': data,
        }
        return result

    def response_delete(self, total_items=1, total_deleted=1):
        result = {
            'success': True,
            'detail': {
                'total_items': total_items,
                'total_deleted': total_deleted,
            },
        }
        return result

    def response_insert(self, total_items=1, total_inserted=1):
        result = {
            'success': True,
            'detail': {
                'total_items': total_items,
                'total_inserted': total_inserted,
            },
        }
        return result

    def decode_to_json(self, data):
        if self.CLIENT_ENCODE:
            response = service_decode_to_json(data)
        else:
            response = json.loads(data)
        return response

    def get_language_header(self, request):
        lang_code = request.META.get('HTTP_MNV_LANGUAGE', self.lang_code)
        self.lang = LANGUAGES_TO_ID.get(lang_code, LANGUAGE_TYPE_VIETNAMESE)
        self.lang_code = ID_TO_LANGUAGES.get(self.lang, ID_TO_LANGUAGES[LANGUAGE_TYPE_VIETNAMESE])


def customize_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    # Now add the HTTP status code to the response.
    if response is not None:
        response.data['success'] = False

        # hardco de toàn bộ eror code cho mobile về 200:
        response.status_code = status.HTTP_200_OK

        client_encode = get_encode_header(context['request'])
        if client_encode:
            response.data = service_encode_from_json(response.data)

        response = Response(data=response.data, status=response.status_code)
    return response
