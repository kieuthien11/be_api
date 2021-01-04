from django.utils.translation import ugettext_lazy as _


POLYGON_TYPE_POINT = 1
POLYGON_TYPE_POLYGON = 2
POLYGON_TYPE = {
    POLYGON_TYPE_POINT: _('Point'),
    POLYGON_TYPE_POLYGON: _('Polygon'),
}
POLYGON_TYPE_CHOICE = ((k, v) for k, v in POLYGON_TYPE.items())
POLYGON_TYPE_LIST = [(k, v) for k, v in POLYGON_TYPE.items()]

URL_MAP_STYLE = "https://images.minerva.vn/Style/"