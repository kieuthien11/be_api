import requests
import json
from django.utils import translation

from library.functions import convert_list_to_string
from library.constant.services import MNV_ENCODE

HEADER = {
    'Content-Type': 'application/json',
    "MNV-ENCODE": MNV_ENCODE,
    # 'Authorization': 'bearer ' + SERVICE_CORE_KEY
}


def request_error(description):
    data = {
        "Error": description,
        "success": False
    }
    return data


def request_api(url, method, content={}, params={}, headers=HEADER):
    if 'MNV-LANGUAGE' in headers:
        headers["MNV-LANGUAGE"] = translation.get_language()

    for key in params.keys():
        if isinstance(params[key], list):
            params[key] = convert_list_to_string(params[key])
    try:
        if method.lower() == 'post':
            response = requests.post(
                url, params=params, data=json.dumps(content), headers=headers, verify=False)
            data = response.content

        elif method.lower() == 'put':
            response = requests.put(
                url, params=params, data=json.dumps(content), headers=headers, verify=False)
            data = response.content

        elif method.lower() == 'get':
            response = requests.get(
                url, params=params, data=json.dumps(content), headers=headers, verify=False)
            data = response.content

    except requests.exceptions.HTTPError as err:
        data = request_error("Http Error: " + err)
    except requests.exceptions.ConnectionError as err:
        data = request_error("Error Connecting: " + err)
    except requests.exceptions.Timeout as err:
        data = request_error("Timeout Error: " + err)
    except requests.exceptions.RequestException as err:
        data = request_error("OOps: Something Else: " + err)

    return data
