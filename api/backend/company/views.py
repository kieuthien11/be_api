from django.db import transaction
from django.db.models import F

from api.base.baseViews import BaseAPIView

from core.company.models import Company
from library.constant.api import SERVICE_CODE_NOT_EXISTS_BODY, SERVICE_CODE_BODY_PARSE_ERROR
from library.functions import convert_to_int


class CompanyViewSet(BaseAPIView):
    def list(self, request, *args, **kwargs):
        company_name = self.request.query_params.get('name', None)
        company_list = Company.objects.all()

        if company_name:
            company_list = company_list.filter(name__icontains=company_name)

        company_list = company_list.annotate(
            company_id=F('id'),
            company_name=F('name'),
            company_description=F('description')
        ).values('company_id', 'company_name', 'company_description')

        self.paginator(company_list)

        return self.response(self.response_paging(list(company_list)))

    def create_or_update(self, request, *args, **kwargs):

        if not request.body:
            return self.response_exception(code=SERVICE_CODE_NOT_EXISTS_BODY)
        try:
            data = self.decode_to_json(request.body)
        except Exception as ex:

            return self.response_exception(code=SERVICE_CODE_BODY_PARSE_ERROR, mess=str(ex))

        check_keys_list = ['company_name', 'company_description']
        key_in_content = list(data.keys())
        key_missing = [key for key in check_keys_list if key not in key_in_content]
        if key_missing:
            return self.validate_exception('Missing ' + ", ".join(str(param) for param in key_missing))

        tra = transaction.savepoint()

        company_name = data.get('company_name', None)
        company_description = data.get('company_description', None)
        company_id = data.get('company_id', None)

        if company_id:
            company = Company.objects.filter(id=company_id).first()
            if not company:
                transaction.savepoint_rollback(tra)
                return self.response_exception(code='SERVICE_CODE_COMPANY_NOT_EXIST')

            company.name = company_name
            company.description = company_description
            company.save()

        else:
            company = Company.objects.create(
                name=company_name,
                description=company_description
            )

        if company:
            transaction.savepoint_commit(tra)
            return self.response(self.response_success({
                'company_id': company.id
            }))
        else:
            transaction.savepoint_rollback(tra)
            return self.response_exception(code="COMPANY_NOT_EXIST")

    def detail_company(self, request, *args, **kwargs):

        company_id = self.request.query_params.get('company_id', None)
        if not company_id:
            return self.validate_exception('Missing company_id')

        company_id = convert_to_int(company_id)
        if not company_id:
            return self.validate_exception('Can not convert company_id to int')

        company = Company.objects.filter(id=company_id)
        if not company:
            return self.response_exception('Company Query does not exist')

        company = company.annotate(
            company_id=F('id'),
            company_name=F('name'),
            company_description=F('description')
        ).values('company_id', 'company_name', 'company_description').first()

        return self.response(self.response_success(company))

    def delete_company(self, request, *args, **kwargs):

        if not request.body:
            return self.response_exception(code=SERVICE_CODE_NOT_EXISTS_BODY)
        try:
            data = self.decode_to_json(request.body)
        except Exception as ex:

            return self.response_exception(code=SERVICE_CODE_BODY_PARSE_ERROR, mess=str(ex))

        company_id = data.get('company_id', None)
        if not company_id:
            return self.validate_exception('Missing company_id')

        company_id = convert_to_int(company_id)
        if not company_id:
            return self.validate_exception('Can not convert company_id to int')

        company = Company.objects.filter(id=company_id)
        if not company:
            return self.response_exception('Company query does not exist')

        company.delete()

        return self.response(self.response_delete())
