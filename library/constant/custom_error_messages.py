PERM_VIEW_TASK = 1

FULL_NAME_EMPTY = 'FULL_NAME_EMPTY'
EMAIL_EXIST = 'EMAIL_EXIST'
EMAIL_NOT_VALID = 'EMAIL_NOT_VALID'
PERMISSION_DENIED = 'PERMISSION_DENIED'
SAME_PASSWORD = 'SAME_PASSWORD'
INVALID_REPEAT_PASSWORD = 'INVALID_REPEAT_PASSWORD'
NEW_PASSWORD_EMPTY = 'NEW_PASSWORD_EMPTY'
NEW_PASSWORD_LESS_THAN_8_CHAR = 'NEW_PASSWORD_LESS_THAN_8_CHAR'
NEW_PASSWORD_GREATER_THAN_25_CHAR = 'NEW_PASSWORD_GREATER_THAN_25_CHAR'
WRONG_PASSWORD = 'WRONG_PASSWORD'
INVALID_LOGIN = 'INVALID_LOGIN'
INVALID_TOKEN = 'INVALID_TOKEN'
USER_NOT_FOUND = 'USER_NOT_FOUND'
DATA_NOT_FOUND = 'DATA_NOT_FOUND'
INACTIVE_USER = 'INACTIVE_USER'
ACTIVATED_USER = 'ACTIVATED_USER'
DISABLED_USER = 'DISABLED_USER'
EXPIRED_TOKEN = 'EXPIRED_TOKEN'
CONDITION_VALUE_ERROR = 'CONDITION_VALUE_ERROR'

CUSTOM_ERROR_MESSAGE = {
    PERMISSION_DENIED: {
        'vi': 'Bạn không có quyền truy cập',
        'en': 'Permission denied',
        'zh-hans': 'Permission denied',
    },
    SAME_PASSWORD: {
        'vi': 'Mật khẩu mới trùng với mật khẩu cũ',
        'en': 'New password and current password are the same',
        'zh-hans': 'New password and current password are the same',
    },
    INVALID_REPEAT_PASSWORD: {
        'vi': 'Nhập lại mật khẩu mới không chính xác',
        'en': 'New password and the repeat one are not the same',
        'zh-hans': 'New password and the repeat one are not the same',
    },
    NEW_PASSWORD_EMPTY: {
        'vi': 'Mật khẩu mới rỗng',
        'en': 'New password is empty',
        'zh-hans': 'New password is empty',
    },
    NEW_PASSWORD_LESS_THAN_8_CHAR: {
        'vi': 'Mật khẩu mới có ít nhất 8 ký tự',
        'en': 'New password is at least 8 characters',
        'zh-hans': 'New password is at least 8 characters',
    },
    NEW_PASSWORD_GREATER_THAN_25_CHAR: {
        'vi': 'Mật khẩu mới có nhiều nhất 25 ký tự',
        'en': 'New password is at most 25 characters',
        'zh-hans': 'New password is at most 25 characters',
    },
    WRONG_PASSWORD: {
        'vi': 'Mật khẩu hiện tại không chính xác',
        'en': 'Current password is wrong',
        'zh-hans': 'Current password is wrong',
    },
    INVALID_LOGIN: {
        'vi': 'Tên đăng nhập hoặc mật khẩu không hợp lệ!',
        'en': 'Invalid username or password',
        'zh-hans': 'Invalid username or password',
    },
    USER_NOT_FOUND: {
        'vi': 'Không tồn tại tài khoản',
        'en': 'User does not exist',
        'zh-hans': 'User does not exist',
    },
    INVALID_TOKEN: {
        'vi': 'Token không hợp lệ',
        'en': 'Invalid token',
        'zh-hans': 'Invalid token',
    },
    DATA_NOT_FOUND: {
        'vi': 'Không tìm thấy dữ liệu',
        'en': 'Data not found',
        'zh-hans': 'Data not found',
    },
    INACTIVE_USER: {
        'vi': 'Tài khoản chưa kích hoạt',
        'en': 'Account is inactive',
        'zh-hans': 'Account is inactive',
    },
    ACTIVATED_USER: {
        'vi': 'Tài khoản đã được kích hoạt',
        'en': 'Account is activated',
        'zh-hans': 'Account is activated',
    },
    DISABLED_USER: {
        'vi': 'Tài khoản bị vô hiệu hóa',
        'en': 'Account is disabled',
        'zh-hans': 'Account is disabled',
    },
    EXPIRED_TOKEN: {
        'vi': 'Token quá hạn',
        'en': 'Token is expired',
        'zh-hans': 'Token is expired',
    },
    CONDITION_VALUE_ERROR: {
        'vi': 'Chi phí phải nhỏ hơn tổng giá trị',
        'en': 'Condition cost must less than sum value',
        'zh-hans': 'Condition cost must less than sum value',
    }

}
