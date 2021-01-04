from django.utils.translation import ugettext_lazy as _

MASTER_TAX_FEE_TYPE_VAT = 1
MASTER_TAX_FEE_TYPE_MAINTENANCE = 2
MASTER_TAX_FEE_TYPE = {
    MASTER_TAX_FEE_TYPE_VAT: _('VAT'),
    MASTER_TAX_FEE_TYPE_MAINTENANCE: _('Maintenance fee')
}
