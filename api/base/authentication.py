from django.db.models import F

from api.base_authentication import BaseBasicAuthentication, BaseTokenAuthentication
from rest_framework import exceptions


from library.constant.api import SERVICE_CODE_HEADER_INVALID, SERVICE_MESSAGE, \
    SERVICE_CODE_NOT_EXISTS_USER, SERVICE_CODE_WRONG_TOKEN, SERVICE_CODE_WRONG_PASSWORD, SERVICE_CODE_EMAIL_DUPLICATE, SERVICE_CODE_NOT_FOUND, SERVICE_CODE_DEVICE_OTP_INVALID

from library.otp import get_otp
from library.authorization import check_developer_login, login_exception, get_language_header


# check token authorize
class TokenAuthentication(BaseTokenAuthentication):
    is_for_banking = False

    def authenticate_credentials(self, user_id, token, request=None):
        # self.check_otp_header(request)

        error_code = None
        user = None

        # if self.is_for_banking:
        #     try:
        #         user = BankingUser.objects.filter(pk=user_id, account_active_flag=True).first()
        #     except:
        #         error_code = INVALID_LOGIN
        # else:
        #     try:
        #         user = Customer.objects.filter(pk=user_id, account_active_flag=True).annotate(full_name=F('name')).first()
        #     except:
        #         error_code = INVALID_LOGIN
        #
        # if not user:
        #     user = None
        #     error_code = INVALID_LOGIN
        #
        # elif token != user.token:
        #     user = None
        #     error_code = INVALID_TOKEN

        setattr(request, 'user', user)
        setattr(request, 'error_code', error_code)
        self.authorize_user(request)
        return user, token

    def authenticate_header(self, request):
        return self.keyword

    def authorize_user(self, request):
        lang_code = get_language_header(request)
        try:
            user = request.user
            error_code = request.error_code
        except:
            fail = {
                'success': False,
                'code': SERVICE_CODE_HEADER_INVALID,
                'detail': SERVICE_MESSAGE[SERVICE_CODE_HEADER_INVALID]}
            raise exceptions.AuthenticationFailed(fail)

        if not user:
            fail = login_exception(error_code, lang_code)
            raise exceptions.AuthenticationFailed(fail)

        return None

    def check_otp_header(self, request):
        if not self.check_device_otp_valid(request):
            fail = {
                'success': False,
                'code': SERVICE_CODE_DEVICE_OTP_INVALID,
                'detail': SERVICE_MESSAGE[SERVICE_CODE_DEVICE_OTP_INVALID]}
            raise exceptions.AuthenticationFailed(fail)
        return None

    def check_device_otp_valid(self, request):
        if request:
            # bypass OTP in dev env.
            if check_developer_login(request):
                pass
            else:
                http_device = request.META.get('HTTP_MNV_DEVICE')

                if not http_device:
                    return False

                otp_cur, otp_pre, otp_next = get_otp()

                try:
                    device_otp = http_device
                except ValueError:
                    return False

                if device_otp not in (otp_cur, otp_pre, otp_next):
                    return False

            return True

        return False


# Login authorize
class BasicAuthentication(BaseBasicAuthentication):

    def authenticate_credentials(self, username, password, request=None):
        credentials = {
            'username': username,
            'password': password
        }
        # user, error_code = self.authorize_user(**credentials)
        # if error_code:
        #     lang_code = get_language_header(request)
        #     fail = login_exception(error_code, lang_code)
        #     raise exceptions.AuthenticationFailed(fail)
        #
        # user.last_login = now()
        # user.save()
        # setattr(request, 'user', user)
        # return user, None  # authentication successful

        return None
    # @staticmethod
    # def authorize_user(**credentials):
    #     try:
    #         user = Customer.objects.filter(username=credentials['username'], account_active_flag=True).first()
    #
    #         # bank
    #         if user is None:
    #             user = BankingUser.objects.filter(username=credentials['username'], account_active_flag=True).first()
    #
    #         if user is None:
    #             return None, INVALID_LOGIN
    #
    #         if user.check_password(credentials['password']):
    #             if user.active_flag:
    #                 if user.email_confirmed_flag:
    #                     return user, None
    #                 else:
    #                     return None, INACTIVE_USER
    #             else:
    #                 return None, DISABLED_USER
    #         else:
    #             if user:
    #                 return None, INVALID_LOGIN
    #             return None, INVALID_LOGIN
    #     except:
    #         return None, INVALID_LOGIN
