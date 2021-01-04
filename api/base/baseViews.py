from django.core.paginator import Paginator, EmptyPage
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import HTTP_HEADER_ENCODING

from api.apiView import APIView
# from api.base.authentication import TokenAuthentication

from library.constant.api import PAGINATOR_PER_PAGE
from library.functions import convert_to_int, search_object_list, unique_key_in_object_list
from library.functions import get_value_list
from library.constant.api import CONTENT_TYPE_JSON

# from superapp.root_local import AUTHENTICATION_SERVICE_KEY


class BaseAPIView(APIView):
    # setting default authentication
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    user = None
    is_paging = False
    per_page = PAGINATOR_PER_PAGE
    page = 1
    total_page = None
    total_record = None
    paging_list = None
    current_page = None
    order_by = 'id'

    def __init__(self):
        super().__init__()
        TokenAuthentication.is_for_banking = False

    def dispatch(self, *args, **kwargs):
        response = super().dispatch(*args, **kwargs)
        # from django.db import connection
        # for query in connection.queries:
        #     print("\n")
        #     print(query["sql"])
        #     print("\n")
        # print(50*"=")
        # print("Total number of queries: ", end="")
        # print(len(connection.queries))
        # print(50*"=")
        return response

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        self.user = request.user
        self.parse_param_common(request)
        self.init_paging()

    def init_paging(self):
        per_page = self.request.query_params.get('limit', None)
        page = self.request.query_params.get('page', None)
        order_by = self.request.query_params.get('order_by', None)
        if type(order_by) is list:
            order_by = ",".join(map(str, self.order_by))
        if order_by and isinstance(order_by, str):
            self.order_by = order_by

        if per_page and per_page.isdigit():
            self.per_page = int(per_page)
        if page and page.isdigit():
            self.page = int(page)

    def paginator(self, query_set):
        is_order = getattr(query_set, 'ordered', None)
        if not is_order:
            query_set = query_set.order_by(self.order_by)

        paginator = Paginator(query_set, per_page=self.per_page)

        self.total_record = paginator.count
        self.total_page = paginator.num_pages
        self.is_paging = True
        try:
            self.paging_list = list(paginator.page(self.page))
        except EmptyPage:
            self.paging_list = []

    def nested_object_list(self, object_list, mapping_key, fields, child_list=False, include_child_null=False):
        if not object_list or len(object_list) == 1 and not any(object_list[0].values()):
            return []

        object_list = self._nested_child_fields(object_list, mapping_key, fields, child_list, include_child_null)
        return object_list

    @staticmethod
    def _nested_child_fields(object_list, mapping_key, field_list, child_list, include_child_null):
        nested_name_list = field_list.keys()
        for key in nested_name_list:
            field = field_list[key]
            assert (field[0][-2:] == 'id'), "First field of child  must be primary key ID"

        if child_list is not False:
            obj_key_list = get_value_list(object_list, mapping_key)
            nested_list_object = search_object_list(child_list, mapping_key, obj_key_list)
            for nested_name in nested_name_list:
                nested_fields = field_list[nested_name]
                for obj in object_list:
                    obj[nested_name] = []
                    if obj[mapping_key] in nested_list_object.keys():
                        nested_list = nested_list_object[obj[mapping_key]]
                        nested_list = [{k: v for k, v in obj.items() if k in nested_fields} for obj in nested_list if (include_child_null or obj[nested_fields[0]] is not None)]
                        nested_list = unique_key_in_object_list(nested_list, nested_fields[0])
                        obj[nested_name] = nested_list
            return object_list
        else:
            obj_list = []
            inserted_key = []
            child_fields = [j for i in [v for v in field_list.values()] for j in i]
            for idx, obj in enumerate(object_list):

                if obj[mapping_key] not in inserted_key:
                    main_obj = {k: v for k, v in obj.items() if k not in child_fields}
                    if mapping_key not in main_obj.keys():
                        main_obj[mapping_key] = obj[mapping_key]

                    main_obj.update({k: list() for k in nested_name_list})
                    obj_list.append(main_obj)
                    inserted_key.append(obj[mapping_key])

                for nested_name in nested_name_list:
                    nested_fields = field_list[nested_name]

                    index = inserted_key.index(obj[mapping_key])
                    if obj[nested_fields[0]] not in get_value_list(obj_list[index][nested_name], nested_fields[0]):
                        nested_obj = {k: v for k, v in obj.items() if k in nested_fields}
                        if include_child_null or nested_obj[nested_fields[0]] is not None:
                            obj_list[index][nested_name].append(nested_obj)

            return obj_list


class BaseAPIAnonymousView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()
    PAGINATOR_PER_PAGE = 20

    user = None
    is_paging = False
    total_page = 1
    total_record = 1
    paging_list = None
    page = 1  # current page
    per_page = PAGINATOR_PER_PAGE  # limit
    order_by = None

    def __init__(self):
        super().__init__()
        TokenAuthentication.is_for_banking = False

    def dispatch(self, *args, **kwargs):
        response = super().dispatch(*args, **kwargs)
        # from django.db import connection
        # for query in connection.queries:
        #     print("\n")
        #     print(query["sql"])
        #     print("\n")
        # print(50*"=")
        # print("Total number of queries: ", end="")
        # print(len(connection.queries))
        # print(50*"=")
        return response

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

        # có bearer trong header thì check token mới hoạt động
        if self.get_authorization_header(request).split():
            self.user = request.user

        # self.check_security_services(request)
        self.parse_param_common(request)
        self.init_paging()

    def init_paging(self):
        per_page = self.request.query_params.get('limit', None)
        page = self.request.query_params.get('page', None)
        self.order_by = self.request.query_params.get('order_by', None)

        if per_page and per_page.isdigit():
            self.per_page = int(per_page)
        if page and page.isdigit():
            self.page = int(page)

    def paginator(self, query_set):
        paginator = Paginator(query_set, per_page=self.per_page)
        print(paginator)
        print('oke')
        self.total_record = paginator.count
        self.total_page = paginator.num_pages
        self.is_paging = True
        try:
            self.paging_list = list(paginator.page(self.page))
        except:
            self.paging_list = []

    def get_content_type_header(self, request):
        content = request.META.get('CONTENT_TYPE', b'')
        try:
            content = content.encode(HTTP_HEADER_ENCODING)
        except:
            content = b''
        return content

    def get_authorization_header(self, request):
        content = request.META.get('HTTP_AUTHORIZATION', b'')
        try:
            content = content.encode(HTTP_HEADER_ENCODING)
        except:
            content = b''
        return content

    def check_token_in_authorization(self, request):
        content = self.get_authorization_header(request).split()
        if content:
            token_type = content[0].decode()  # covert b to s
            token = content[1].decode()

            # if token_type and AUTHENTICATION_SERVICE_KEY == token:
            #     return True
        return False

    def check_security_services(self, request):
        is_token_validated = self.check_token_in_authorization(request)
        if not is_token_validated:
            self.response_exception(code=103)

    def nested_object_list(self, object_list, mapping_key, fields, child_list=False, include_child_null=False):
        if not object_list or len(object_list) == 1 and not any(object_list[0].values()):
            return []

        object_list = self._nested_child_fields(object_list, mapping_key, fields, child_list, include_child_null)
        return object_list

    @staticmethod
    def _nested_child_fields(object_list, mapping_key, field_list, child_list, include_child_null):
        nested_name_list = field_list.keys()
        for key in nested_name_list:
            field = field_list[key]
            assert (field[0][-2:] == 'id'), "First field of child  must be primary key ID"

        if child_list is not False:
            obj_key_list = get_value_list(object_list, mapping_key)
            nested_list_object = search_object_list(child_list, mapping_key, obj_key_list)
            for nested_name in nested_name_list:
                nested_fields = field_list[nested_name]
                for obj in object_list:
                    obj[nested_name] = []
                    if obj[mapping_key] in nested_list_object.keys():
                        nested_list = nested_list_object[obj[mapping_key]]
                        nested_list = [{k: v for k, v in obj.items() if k in nested_fields} for obj in nested_list if (include_child_null or obj[nested_fields[0]] is not None)]
                        nested_list = unique_key_in_object_list(nested_list, nested_fields[0])
                        obj[nested_name] = nested_list
            return object_list
        else:
            obj_list = []
            inserted_key = []
            child_fields = [j for i in [v for v in field_list.values()] for j in i]
            for idx, obj in enumerate(object_list):

                if obj[mapping_key] not in inserted_key:
                    main_obj = {k: v for k, v in obj.items() if k not in child_fields}
                    if mapping_key not in main_obj.keys():
                        main_obj[mapping_key] = obj[mapping_key]

                    main_obj.update({k: list() for k in nested_name_list})
                    obj_list.append(main_obj)
                    inserted_key.append(obj[mapping_key])

                for nested_name in nested_name_list:
                    nested_fields = field_list[nested_name]

                    index = inserted_key.index(obj[mapping_key])
                    if obj[nested_fields[0]] not in get_value_list(obj_list[index][nested_name], nested_fields[0]):
                        nested_obj = {k: v for k, v in obj.items() if k in nested_fields}
                        if include_child_null or nested_obj[nested_fields[0]] is not None:
                            obj_list[index][nested_name].append(nested_obj)

            return obj_list
