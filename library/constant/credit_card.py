
CREDIT_CARD_TYPE_VISA = 1
CREDIT_CARD_TYPE_MASTERCARD = 2
CREDIT_CARD_TYPE_AMEX = 3
CREDIT_CARD_TYPE_JCB = 4
CREDIT_CARD_TYPE = {
    CREDIT_CARD_TYPE_VISA: 'Visa',
    CREDIT_CARD_TYPE_MASTERCARD: 'Mastercard',
    CREDIT_CARD_TYPE_AMEX: 'Amex',
    CREDIT_CARD_TYPE_JCB: 'Jcb',
}
CREDIT_CARD_TYPE_CHOICE = ((k, v) for k, v in CREDIT_CARD_TYPE.items())
CREDIT_CARD_TYPE_LIST = [(k, v) for k, v in CREDIT_CARD_TYPE.items()]
