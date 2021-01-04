import re, json

from django.urls import reverse


from library.functions import now
from library.constant.reset_password import RESET_PASSWORD_TYPE_SELF, RESET_PASSWORD_TYPE_CUSTOMER, RESET_PASSWORD_TYPE_BANKING_USER
from library.service.functions import request_api, HEADER_UNIPRIME
from library.service.service_urls import SERVICE_UNIPRIME_FORGOT_PASSWORD

from django.core.mail import send_mail


###############################################################################################
# INPUT
###############################################################################################
# seft reset password:
#   request=self.request, type_reset_pass=RESET_PASSWORD_TYPE_SELF, email='example@example.com'

# customer (distribution channel contact, distribution channel seller, customer) reset password:
#   request=self.request, type_reset_pass=RESET_PASSWORD_TYPE_CUSTOMER, customer_or_banking_user_id=1

# banking user reset password:
#   request=self.request, type_reset_pass=RESET_PASSWORD_TYPE_BANKING_USER, customer_or_banking_user_id=1
###############################################################################################

###############################################################################################
# OUTPUT: dict {'success': True, 'detail': 'This is an output message'}
###############################################################################################
# 'success': True: success
# 'success': False: fail
###############################################################################################

def send_email_reset_password(request, type_reset_pass, email=None, customer_or_banking_user_id=None):
    if type_reset_pass == RESET_PASSWORD_TYPE_SELF:
        if email is None:
            return {
                'success': False,
                'detail': 'email must be passed in when seft reset password'
            }

        if not isinstance(email, str):
            return {
                'success': False,
                'detail': 'email must be a string'
            }

        email = email.lower()

        if re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email) is None:
            return {
                'success': False,
                'detail': 'email is not valid'
            }

        # TODO: đợt chốt và thêm SERVICE_UNIPRIME_FORGOT_PASSWORD bên uniprime mobile
        try:
            response_forgot_password_uniprime = json.loads(request_api(
                url=SERVICE_UNIPRIME_FORGOT_PASSWORD,
                method='POST',
                content={'email': email},
                headers=HEADER_UNIPRIME
            ))
            if response_forgot_password_uniprime['success']:
                return {
                    'success': True,
                    'detail': 'send email reset password success'
                }

        except:
            return {
                'success': False,
                'detail': 'call to uniprime api error'
            }

    elif type_reset_pass == RESET_PASSWORD_TYPE_CUSTOMER or type_reset_pass == RESET_PASSWORD_TYPE_BANKING_USER:
        if customer_or_banking_user_id is None:
            return {
                'success': False,
                'detail': 'customer_or_banking_user_id must be passed in when reset password customer'
            }

        if not isinstance(customer_or_banking_user_id, int):
            return {
                'success': False,
                'detail': 'customer_or_banking_user_id must be an integer'
            }

        if type_reset_pass == RESET_PASSWORD_TYPE_CUSTOMER:
            model = Customer
        else:
            model = BankingUser

        try:
            customer_or_banking_user = model.objects.get(id=customer_or_banking_user_id)
        except model.DoesNotExist as ex:
            return {
                'success': False,
                'detail': str(ex)
            }

        if customer_or_banking_user.username is None:
            return {
                'success': False,
                'detail': 'customer_or_banking_user_id does not have account before'
            }

        if type_reset_pass == RESET_PASSWORD_TYPE_CUSTOMER:
            nick_name = customer_or_banking_user.name
        else:
            nick_name = customer_or_banking_user.full_name

        if nick_name is None or nick_name == '':
            nick_name = 'user'

        email = customer_or_banking_user.email
        key_reset_pass = customer_or_banking_user.reset_key_reset_password(now())

        host_url = request.build_absolute_uri(reverse('reset_pass', kwargs={'key': key_reset_pass}))
        html_message = '<p>Dear ' + nick_name + ',</p>' \
                                                '<p>&nbsp;</p>' \
                                                '<p>We have received your request to reset your password.</p>' \
                                                '<p>Please click on the link below to get you in the door:</p>' \
                                                '<p>Link <a href="' + host_url + '">' + host_url + '</a></p>' \
                                                                                                   "<p>Don't leave it to late through, this link is only available for 24 hours.</p>" \
                                                                                                   '<p>&nbsp;</p>' \
                                                                                                   '<p>Thanks,</p>' \
                                                                                                   '<p>Admin Team</p>'
        try:
            send_mail(
                'Reset your password',
                '',
                'EMAIL_HOST_STRING',
                [email],
                html_message=html_message
            )

            return {
                'success': True,
                'detail': 'send email reset password success'
            }
        except Exception:
            return {
                'success': False,
                'detail': 'send email reset password fail',
            }

    else:
        return {
            'success': False,
            'detail': 'type_reset_pass is not valid',
        }