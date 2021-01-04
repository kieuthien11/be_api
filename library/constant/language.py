from django.utils.translation import ugettext_lazy as _


LANGUAGES = (
    ('vi', _('Vietnamese')),
    ('en', _('English')),
    ('zh-hans', _('简体中文')),
)

LANGUAGE_TYPE_VIETNAMESE = 1
LANGUAGE_TYPE_ENGLISH = 2
LANGUAGE_TYPE_CHINESE = 3

LANGUAGE_TYPE = {
    LANGUAGE_TYPE_VIETNAMESE: _('Vietnamese'),
    LANGUAGE_TYPE_ENGLISH: _('English'),
    LANGUAGE_TYPE_CHINESE: _('简体中文'),
}
LANGUAGE_TYPE_CHOICE = ((k, v) for k, v in LANGUAGE_TYPE.items())
LANGUAGE_TYPE_LIST = [(k, v) for k, v in LANGUAGE_TYPE.items()]

LANGUAGES_TO_ID = {
    'vi': LANGUAGE_TYPE_VIETNAMESE,
    'en': LANGUAGE_TYPE_ENGLISH,
    'zh-hans': LANGUAGE_TYPE_CHINESE
}

ID_TO_LANGUAGES = {
    LANGUAGE_TYPE_VIETNAMESE: 'vi',
    LANGUAGE_TYPE_ENGLISH: 'en',
    LANGUAGE_TYPE_CHINESE: 'zh-hans'
}
