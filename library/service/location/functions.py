import json
from library.service.service_urls import SERVICE_SYSTEM_FIND_COUNTRY, SERVICE_SYSTEM_FIND_PROVINCE, SERVICE_SYSTEM_FIND_DISTRICT, \
    SERVICE_SYSTEM_FIND_WARD, SERVICE_UNIPRIME_PROVINCE_FILTER \
    , SERVICE_SYSTEM_PROVINCE_ALL_URL, SERVICE_SYSTEM_SEARCH_ALL, SERVICE_UNIPRIME_DISTRICT_FILTER, \
    SERVICE_SYSTEM_DISTRICT_FROM_PROVINCE_URL, SERVICE_UNIPRIME_WARD_FILTER, SERVICE_SYSTEM_WARD_FROM_DISTRICT_URL, \
    SERVICE_SYSTEM_SEARCH_CURRECY_RATE, SERVICE_SYSTEM_REGION_ALL_URL, SERVICE_SYSTEM_COUNTRIES_ALL_URL

from library.service.functions import request_api


def check_location_valid(province_id, district_id, ward_id):
    if province_id and json.loads(get_province(province_id=province_id))['success'] is False:
        return False

    if province_id and district_id and json.loads(get_district(province_id=province_id, district_id=district_id))[
        'success'] is False:
        return False

    if district_id and ward_id and json.loads(get_ward(district_id=district_id, ward_id=ward_id))[
        'success'] is False:
        return False
    return True


def get_country_name(country_id):
    response = request_api(SERVICE_SYSTEM_FIND_COUNTRY, 'POST', content={"country_id": [country_id]})
    try:
        province_dict = json.loads(response)["data"][0]
        return province_dict.get('name')
    except:
        return ""


def get_province_name(province_id):
    response = request_api(SERVICE_SYSTEM_FIND_PROVINCE, 'POST', content={"province_id": [province_id]})
    try:
        province_dict = json.loads(response)["data"][0]
        return province_dict.get('name')
    except:
        return ""


def get_district_name(district_id):
    response = request_api(SERVICE_SYSTEM_FIND_DISTRICT, 'POST', content={"district_id": [district_id]})
    try:
        province_dict = json.loads(response)["data"][0]
        return province_dict.get('name')
    except:
        return ""


def get_ward_name(ward_id):
    response = request_api(SERVICE_SYSTEM_FIND_WARD, 'POST', content={"ward_id": ward_id})
    try:
        province_dict = json.loads(response)["data"][0]
        return province_dict.get('name')
    except:
        return ""


def find_province(province_id):
    response = request_api(SERVICE_SYSTEM_FIND_PROVINCE, 'POST', content={"province_id": province_id})
    try:
        return json.loads(response)["data"]
    except:
        return ""


def find_district(district_id):
    response = request_api(SERVICE_SYSTEM_FIND_DISTRICT, 'POST', content={"district_id": district_id})
    try:
        return json.loads(response)["data"]
    except:
        return ""


def find_ward(ward_id):
    response = request_api(SERVICE_SYSTEM_FIND_WARD, 'POST', content={"ward_id": ward_id})
    try:
        return json.loads(response)["data"]
    except:
        return ""


def get_province(province_id=None, has_project=False):
    if has_project:
        province_list = request_api(SERVICE_UNIPRIME_PROVINCE_FILTER, 'GET')
    else:
        data = {}
        if province_id:
            data["province_id"] = province_id

        province_list = request_api(SERVICE_SYSTEM_PROVINCE_ALL_URL, 'POST', content=data)

    return province_list


#
def get_country():
    countries = request_api(SERVICE_SYSTEM_COUNTRIES_ALL_URL, 'POST')
    return countries


def get_region(region_id=None):
    if region_id:
        data = {"region_id": int(region_id)}
        region_list = request_api(SERVICE_SYSTEM_REGION_ALL_URL, 'POST', content=data)
    else:
        region_list = request_api(SERVICE_SYSTEM_REGION_ALL_URL, 'POST')
    return region_list


def get_district(province_id, district_id=None, has_project=False):
    if has_project:
        district_list = request_api(SERVICE_UNIPRIME_DISTRICT_FILTER, 'GET', params={
            "province_id": province_id
        })
    else:
        data = {"province_id": province_id}
        if district_id:
            data["district_id"] = district_id

        district_list = request_api(SERVICE_SYSTEM_DISTRICT_FROM_PROVINCE_URL, 'POST', content=data)

    return district_list


def get_ward(district_id=None, ward_id=None, has_project=False):
    if has_project:
        ward_list = request_api(SERVICE_UNIPRIME_WARD_FILTER, 'GET', params={
            "district_id": district_id
        })
    else:
        data = {}
        if district_id:
            data["district_id"] = district_id
        if ward_id:
            data['ward_id'] = ward_id

        ward_list = request_api(SERVICE_SYSTEM_WARD_FROM_DISTRICT_URL, 'POST', content=data)

    return ward_list


def get_location_point_from_address(address):
    if address:
        response = request_api(
            url=SERVICE_SYSTEM_SEARCH_ALL,
            method='post',
            content={
                'Keyword': address
            }
        )

        if response:
            data = json.loads(response)

            if data['success'] and data['total_count'] >= 1:
                point_data = data['data'][0]

                if point_data:
                    return {
                        'lat': point_data['Latitude'],
                        'lon': point_data['Longitude']
                    }

    return None


def get_currency_rate_from_vcb_vnd(target_currency):
    if target_currency:
        response = request_api(
            url=SERVICE_SYSTEM_SEARCH_CURRECY_RATE,
            method='GET',
            params={
                "base": target_currency
            }
        )

        if response:
            data = json.loads(response)
            if data['success']:
                data = data['data']
                return data

    return None


def get_dict_province(list_province):
    try:
        list_province = json.loads(
            request_api(
                url=SERVICE_SYSTEM_FIND_PROVINCE,
                method="POST",
                content={"province_id": list_province}
            )
        )['data']
    except:
        list_province = list()

    dict_province = dict()
    for province in list_province:
        dict_province.update({province['province_id']: province['name']})

    return dict_province


def get_dict_district(list_district):
    try:
        list_district = json.loads(
            request_api(
                url=SERVICE_SYSTEM_FIND_DISTRICT,
                method="POST",
                content={"district_id": list_district}
            )
        )['data']
    except:
        list_district = list()

    dict_district = dict()
    for district in list_district:
        dict_district.update({district['district_id']: district['name']})

    return dict_district


def get_dict_ward(list_ward):
    try:
        list_ward = json.loads(
            request_api(
                url=SERVICE_SYSTEM_FIND_WARD,
                method="POST",
                content={"ward_id": list_ward}
            )
        )['data']
    except:
        list_ward = list()

    dict_ward = dict()
    for ward in list_ward:
        dict_ward.update({ward['ward_id']: ward['name']})

    return dict_ward


def get_full_address(short_address, ward_id, district_id, province_id):
    dict_province = get_dict_province([province_id])
    dict_district = get_dict_district([district_id])
    dict_ward = get_dict_ward([ward_id])

    address = short_address if short_address else ''
    ward_name = dict_ward.get(ward_id) if dict_ward.get(ward_id) else ''
    district_name = dict_district.get(district_id) if dict_district.get(district_id) else ''
    province_name = dict_province.get(province_id) if dict_province.get(province_id) else ''

    if not address and not ward_name and not district_name and not province_name:
        return None
    else:
        return ', '.join([temp for temp in [address, ward_name, district_name, province_name] if temp])
