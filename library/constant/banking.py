from django.utils.translation import ugettext_lazy as _

BANKING_GROUP_VIETNAM_BANK_FOR_SOCIAL_POLICIES = 1      # Ngân hàng Chính sách xã hội
BANKING_GROUP_STATE_COMMERCIAL_BANKS = 2                # Ngân hàng thương mại nhà nước
BANKING_GROUP_JOINT_STOCK_COMMERCIAL_BANK = 3           # Ngân hàng thương mại cổ phần
BANKING_GROUP_FOREIGN_BANK = 4                          # Ngân hàng 100% vốn nước ngoài
BANKING_GROUP_JOINT_VENTURE_BANK = 5                    # Ngân hàng liên doanh

BANKING_GROUP = {
    BANKING_GROUP_VIETNAM_BANK_FOR_SOCIAL_POLICIES: _('Vietnam Bank For Social Policies'),
    BANKING_GROUP_STATE_COMMERCIAL_BANKS: _('State Commercial Banks'),
    BANKING_GROUP_JOINT_STOCK_COMMERCIAL_BANK: _('Joint-Stock Commercial Bank'),
    BANKING_GROUP_FOREIGN_BANK: _('100% Foreign Owned Bank'),
    BANKING_GROUP_JOINT_VENTURE_BANK: _('Joint-Venture Bank'),
}
BANKING_GROUP_CHOICE = ((k, v) for k, v in BANKING_GROUP.items())
BANKING_GROUP_LIST = [(k, v) for k, v in BANKING_GROUP.items()]

#############################################################
# dùng để tính toán thời gian vay tối thiểu
# FIXME: hard code
BANKING_POLICY_LOAN_PERIOD_MASTER_UNIT_TYPE_YEAR = 16
BANKING_POLICY_LOAN_PERIOD_MASTER_UNIT_TYPE_MONTH = 17
BANKING_POLICY_LOAN_PERIOD_MASTER_UNIT_TYPE_DAY = 19