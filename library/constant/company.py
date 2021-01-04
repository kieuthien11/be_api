from django.utils.translation import ugettext_lazy as _


COMPANY_TYPE_AGENT = 1
COMPANY_TYPE_INTERNAL = 2

COMPANY_TYPE = {
    COMPANY_TYPE_AGENT: _('Agent'),
    COMPANY_TYPE_INTERNAL: _('Internal'),
}
COMPANY_TYPE_CHOICE = ((k, v) for k, v in COMPANY_TYPE.items())
COMPANY_TYPE_LIST = [(k, v) for k, v in COMPANY_TYPE.items()]
