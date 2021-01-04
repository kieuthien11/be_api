import math
import re
import sys
import json
from datetime import date, timedelta, datetime
from dateutil.parser import parse
from cryptography.fernet import Fernet

from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils.translation import get_language
# from webs.messages import MESSAGE_DICTIONARY
from django.contrib.postgres.fields.jsonb import KeyTextTransform
from django.db import models
from django.db.models.functions import Cast
from collections import OrderedDict
from rest_framework import exceptions

from PIL import Image
from math import isnan

from library.constant.api import SERVICE_MESSAGE
from library.constant.custom_error_messages import CUSTOM_ERROR_MESSAGE
from library.constant.services import PASSWORD_ENCODE_KEY


def merge_dicts(dict1, dict2):
    for k in set(dict1.keys()).union(dict2.keys()):
        if k in dict1 and k in dict2:
            if isinstance(dict1[k], dict) and isinstance(dict2[k], dict):
                yield (k, dict(merge_dicts(dict1[k], dict2[k])))
            else:
                yield (k, dict2[k])
        elif k in dict1:
            yield (k, dict1[k])
        else:
            yield (k, dict2[k])


def validate_image(fieldfile_obj):
    im = Image.open(fieldfile_obj.file)
    im.verify()

    width, height = im.size
    file_size = 1

    megabyte_limit = 2.0
    if file_size > megabyte_limit * 1024 * 1024:
        raise ValidationError("Max file size is %sMB" % str(megabyte_limit))


def today():
    return date.today()


def day_add(time, number):
    try:
        return time + timedelta(days=number)
    except (ValueError, TypeError):
        return None


def day_sub(time, number):
    try:
        return time - timedelta(days=number)
    except (ValueError, TypeError):
        return None


def now():
    return datetime.now()


def convert_string_to_day(string, default=None):
    try:
        return datetime.strptime(string, '%Y-%m-%d')
    except (ValueError, TypeError):
        return default


def convert_string_to_bool(string=None, default=False):
    if string:
        if isinstance(string, bool):
            return string
        try:
            string = int(string)
        except:
            pass
        if isinstance(string, int):
            if 1 == string:
                return True
            else:
                return False
        if isinstance(string, str):
            string = string.strip().lower()
            if 'true' == string:
                return True
            else:
                return False
        return default
    else:
        return default


def round_down(number, point=1):
    multiplier = 10 ** point
    return math.floor(number * multiplier) / multiplier


def convert_string_to_bool_or_none(string=None, default=None):
    if string:
        if isinstance(string, bool):
            return string
        if isinstance(string, str):
            string = string.strip().lower()
            if 'true' == string:
                return True
            elif 'none' == string:
                return None
            else:
                return False
        return default
    else:
        return default


def convert_to_int(string, default=0):
    try:
        return int(round(float(string), 0))
    except:
        return default


def convert_string_to_int(string, default=None):
    try:
        return int(string)
    except:
        return default


def convert_to_int_or_list(string, default=None):
    _data = default
    try:
        _data = int(string)
    except:
        _data = convert_string_to_list(string, None)
    return _data


def convert_string_to_float(string, default=None):
    try:
        return float(string)
    except:
        return default


def convert_string_to_list(string, default=None):
    try:
        project_sale_status = list(json.loads(string.replace("'", '"')))
    except:
        project_sale_status = default
    return project_sale_status


def convert_dong_to_billion_dong(number, decimal=2, default=0):
    try:
        return round(number / 10 ** 9, decimal)
    except:
        return default



def convert_billion_dong_to_dong(number, default=0):
    try:
        return number * (10 ** 9)
    except:
        return default


def convert_list_to_string(list, default="[]"):
    try:
        listToStr = "[" + ','.join(map(str, [i for i in list if i])) + "]"
        return listToStr
    except:
        return default


def convert_to_bool(boolean_str, default=False):
    try:
        boolean_str = boolean_str.lower().strip()
        if boolean_str == 'true':
            return True
        return False
    except:
        return default


def convert_to_float(string, default=0.0):
    try:
        str_float = str(string)
        if str_float.lower() == "nan":
            str_float = None
        return round(float(str_float), 2)
    except:
        return default


def convert_to_dict(string, default={}):
    try:
        return json.loads(string)
    except:
        return default


def end_a_day(_date):
    try:
        to_day = _date.strftime("%d/%m/%Y")
    except AttributeError:
        return None

    _time = datetime.strptime(
        '{} 23:59:59'.format(to_day), '%d/%m/%Y %H:%M:%S')

    return _time


def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + timedelta(days=4)
    return next_month - timedelta(days=next_month.day)


def string_to_time(_string, _format='%d/%m/%Y %H:%M:%S'):
    try:
        return datetime.strptime(_string, _format)
    except (ValueError, IndexError, AttributeError):
        return None


def time_to_string(_time, _format='%d/%m/%Y %H:%M:%S'):
    if _time:
        return _time.strftime(_format)
    return ''


def is_email_valid(email):
    pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'

    regex = re.compile(pattern)

    if email is None or (email is not None and regex.search(email)):
        return True
    else:
        return False


def format_email(email):
    if email:
        email = email.lower()
        email = email.strip()
        return email
    return None


def format_name(name):
    if name:
        name = name.replace('\b', '')
        return name.strip().lower()
    return None


def format_mobile(mobile):
    if mobile:
        mobile = mobile.strip()
        mobile = mobile.replace('.', '')
        mobile = mobile.replace(',', '')
        mobile = mobile.replace('-', '')
        mobile = mobile.replace(' ', '')
        return mobile
    return None


def is_mobile_valid(mobile):
    pattern = '^(0)+([0-9]{9})$'
    regex = re.compile(pattern)

    if mobile is None or (mobile is not None and regex.search(mobile)):
        return True
    else:
        return False


def is_valid_id_number(id_number):
    pattern = '^([0-9]{9}|[0-9]{12}|(?!^0+$)[a-zA-Z0-9]{3,20})$'
    regex = re.compile(pattern)
    if id_number and regex.search(str(id_number)):
        return True
    else:
        return False


def check_json_load_key_exists(key, json_loads):
    if key in json_loads.keys():
        return json_loads.get(key)
    return None


def get_value_list(list, key):
    try:
        value_list = [obj[key] for obj in list]
        return value_list
    except Exception as e:
        return []


def get_dict_list(object_list, key, value):
    try:
        con = [obj for obj in object_list if obj[key] == value]
        return con
    except:
        return []


def get_value_jsonField(key, column, type=None):
    if type is None:
        type = models.IntegerField()
    return Cast(KeyTextTransform(key, column), type)


def search_object_list(object_list, mapping_key, mapping_value_list):
    try:
        result = dict()
        inserted_key = []
        for obj in object_list:
            if obj[mapping_key] not in inserted_key and obj[mapping_key] in mapping_value_list:
                result[obj[mapping_key]] = []
                inserted_key.append(obj[mapping_key])
            if obj[mapping_key] in inserted_key:
                result[obj[mapping_key]].append(obj)

        return result
    except:
        return dict()


def unique_key_in_object_list(object_list, key):
    key_list = []
    result = []
    for obj in object_list:
        if obj[key] not in key_list:
            result.append(obj)
            key_list.append(obj[key])
    return result


def get_character_first(str):
    s = str.split(' ')
    text = ""
    for i in s:
        text += i[0]
    return text


def roman_number(num):
    roman = OrderedDict()
    roman[1000] = "M"
    roman[900] = "CM"
    roman[500] = "D"
    roman[400] = "CD"
    roman[100] = "C"
    roman[90] = "XC"
    roman[50] = "L"
    roman[40] = "XL"
    roman[10] = "X"
    roman[9] = "IX"
    roman[5] = "V"
    roman[4] = "IV"
    roman[1] = "I"

    def roman_num(num):
        num = int(num) if isinstance(num, int) or num.isdigit() else 0
        for r in roman.keys():
            x, y = divmod(num, r)
            yield roman[r] * x
            num -= (r * x)
            if num <= 0:
                break

    return "".join([a for a in roman_num(num)])


def validate_exception(text=None, code=None):
    fail = {
        'success': False,
        'detail': text,
    }
    if code:
        try:
            fail['detail'] = SERVICE_MESSAGE[code]
        except (ValueError, KeyError):
            fail['detail'] = ''

        fail['code'] = code
    raise exceptions.ValidationError(fail)


def validate_type_int(**kwargs):
    assert isinstance(kwargs, dict)
    for key, value in kwargs.items():
        if isinstance(value, int):
            try:
                data = int(value)
            except:
                validate_exception("%s type is int" % str(key))
        if isinstance(value, list):
            for temp in value:
                try:
                    data = int(temp)
                except:
                    validate_exception("items in %s type is int" % str(key))


def format_integer(value):
    try:

        _value = int(value) if value else 0

        return ("{:,}".format(_value).replace(',', '.')) if _value != 0 else ''
    except:
        return "N/A"


def convert_character(text):
    patterns = {
        '[àáảãạăắằẵặẳâầấậẫẩ]': 'a',
        '[đ]': 'd',
        '[èéẻẽẹêềếểễệ]': 'e',
        '[ìíỉĩị]': 'i',
        '[òóỏõọôồốổỗộơờớởỡợ]': 'o',
        '[ùúủũụưừứửữự]': 'u',
        '[ỳýỷỹỵ]': 'y'
    }
    output = text
    for regex, replace in patterns.items():
        output = re.sub(regex, replace, output)
        # deal with upper case
        output = re.sub(regex.upper(), replace.upper(), output)
    return output


def encrypt_password(password):
    fernet = Fernet(PASSWORD_ENCODE_KEY.encode())
    encrypted_password = fernet.encrypt(str(password).encode())
    return encrypted_password.decode()


def decrypt_password(encrypted_password, default=''):
    try:
        fernet = Fernet(PASSWORD_ENCODE_KEY)
        decrypted_password = fernet.decrypt(encrypted_password.encode())
        return decrypted_password.decode()
    except:
        return default


def sizeof_fmt(num, suffix='B'):
    if num is None:
        return '0KB'
    if num:
        for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
            if abs(num) < 1024.0:
                return "{}{}{}".format(round(num), unit, suffix)
            num /= 1024.0
        return "{}{}".format(num, suffix)
    else:
        return "0KB"


def format_float(value, default_value=''):
    try:
        _value = round(float(value), 2) if value else 0
        return ('{:_.2f}'.format(_value).replace('.', ',').replace('_', '.')) if _value != 0 else default_value
    except:
        return default_value


def format_int(value):
    try:
        _value = int(value) if value else 0
        return ('{:_.0f}'.format(_value).replace('.', ',').replace('_', '.')) if _value != 0 else ''
    except:
        return ''


def format_area(total_area):
    formated_float = format_float(total_area)
    if formated_float:
        return '{} {}'.format(formated_float, str('m\u00b2'))
    else:
        return '-'
