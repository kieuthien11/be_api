from rest_framework.utils import json


def service_response_to_json(data):
    response = json.loads(data)
    return response