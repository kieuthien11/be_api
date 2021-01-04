from django.utils.translation import ugettext_lazy as _

URL_BACKEND_API = 'api.backend.v1.'

CONTENT_TYPE_JSON = b'application/json'
CONTENT_TYPE_FROM_DATA = b'multipart/form-data'
CONTENT_TYPE_IMAGE = b'image/png'

PAGINATOR_PER_PAGE = 20

SERVICE_CODE_DEVICE_INVALID = 100  # thiết bị không hợp lệ
SERVICE_CODE_NOT_EXISTS_USER = 101  # không tồn tại User
SERVICE_CODE_WRONG_PASSWORD = 102  # Sai mật khẩu
SERVICE_CODE_WRONG_TOKEN = 103  # Sai token
SERVICE_CODE_USER_IS_LOCKED = 104  # Tài khoản bị Aber khóa
SERVICE_CODE_USER_NOT_ACTIVE = 105  # Tài khoản chưa kích hoạt
SERVICE_CODE_DEVICE_OTP_INVALID = 106  # sai OTP

SERVICE_CODE_SEND_EMAIL_FAIL = 199  # gửi mail để reset pass khi người dùng quên mật khẩu thất bại
SERVICE_CODE_NOT_FOUND = 200  # data tìm không thấy
SERVICE_CODE_ERROR = 201  # Dùng chung
SERVICE_CODE_ERROR_SEND_SMS = 202  # số di động không hợp lệ
SERVICE_CODE_BODY_PARSE_ERROR = 203  # parse body từ client
SERVICE_CODE_NOT_EXISTS_BODY = 204  # body client gửi lên không tồn tại
SERVICE_CODE_TOKEN_INVALID = 205  # dùng trong service gọi sms otp của khách hàng
SERVICE_CODE_HEADER_INVALID = 206  # header không chứa thông tin nhận diện
SERVICE_CODE_EMAIL_DUPLICATE = 207  # email đã tồn tại
SERVICE_CODE_EMAIL_INVALID = 208  # email không hợp lệ
SERVICE_CODE_CUSTOMER_NOT_EXIST = 209  # customer không tồn tại
SERVICE_CODE_LOCATION_INVALID = 214  # location is invalid
SERVICE_CODE_PASSWORD_MISMATCH = 217  # password is not matched
SERVICE_CODE_PASSWORD_INVALID = 226
SERVICE_CODE_PASSWORD_MUST_DIFFERENCE = 250

SERVICE_CODE_SPAM = 400

# -- Dictionary --
SERVICE_MESSAGE = {
    SERVICE_CODE_DEVICE_INVALID: 'Thiết bị không hợp lệ',
    SERVICE_CODE_DEVICE_OTP_INVALID: 'OTP không hợp lệ',
    SERVICE_CODE_NOT_EXISTS_USER: 'Không tồn tại tài khoản',
    SERVICE_CODE_WRONG_PASSWORD: 'Sai thông tin đăng nhập',
    SERVICE_CODE_WRONG_TOKEN: 'Token không hợp lệ',
    SERVICE_CODE_USER_NOT_ACTIVE: 'Tài khoản chưa kích hoạt. Vui lòng liên hệ Admin.',
    SERVICE_CODE_USER_IS_LOCKED: 'Tài khoản của bạn bị khóa. Vui lòng liên hệ Admin.',
    SERVICE_CODE_NOT_FOUND: 'Không tồn tại dữ liệu',
    SERVICE_CODE_SPAM: 'Spam',
    SERVICE_CODE_HEADER_INVALID: 'Header không hợp lệ',
    SERVICE_CODE_BODY_PARSE_ERROR: 'Body parse lỗi',
    SERVICE_CODE_NOT_EXISTS_BODY: 'Không tìm thấy dữ liệu ...',
    SERVICE_CODE_EMAIL_DUPLICATE: 'Email này đã tồn tại trong hệ thống',
    SERVICE_CODE_EMAIL_INVALID: "Email không hợp lệ",
    SERVICE_CODE_CUSTOMER_NOT_EXIST: "Customer không tồn tại trong hệ thống",
    SERVICE_CODE_LOCATION_INVALID: "Thông tin của tỉnh, phường, xã không hợp lệ",
    SERVICE_CODE_PASSWORD_MISMATCH: "Mật khẩu không trùng khớp",
    SERVICE_CODE_PASSWORD_INVALID: "Mật khẩu không hơp lệ",
    SERVICE_CODE_PASSWORD_MUST_DIFFERENCE: "Mật khẩu mới phải khác mật khẩu cũ",

}

# --- Sort method ---

ORDER_BY_ASC = 1
ORDER_BY_DESC = 2

SORT_TYPE = {
    ORDER_BY_ASC: _('asc'),
    ORDER_BY_DESC: _('desc'),
}

SORT_TYPE_CHOICE = ((k, v) for k, v in SORT_TYPE.items())
SORT_TYPE_LIST = [(k, v) for k, v in SORT_TYPE.items()]

SORT_TYPE_TO_ID = {
    'asc': ORDER_BY_ASC,
    'desc': ORDER_BY_DESC
}
