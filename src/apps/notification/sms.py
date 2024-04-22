from apps.core.utils import send_sms, get_host_url


class NotificationUser:

    @classmethod
    def handler_payment_successfully_user(cls, notification, phonenumber):
        pattern = 'ar0prdkncw4dk9l'
        send_sms(phonenumber, pattern, {
            'notification_url': get_host_url(notification.get_link()),
            'user_name': notification.to_user.get_full_name()
        })

    @classmethod
    def handler_new_payment_admin(cls, notification, phonenumber):
        pattern = 'ar0prdkncw4dk9l'
        send_sms(phonenumber, pattern, {
            'notification_url': get_host_url(notification.get_link()),
            'user_name': notification.to_user.get_full_name()
        })

    @classmethod
    def handler_custom_product_added_to_cart(cls, notification, phonenumber):
        pattern = 'ar0prdkncw4dk9l'
        send_sms(phonenumber, pattern, {
            'user_name': notification.to_user.get_full_name()
        })

    @classmethod
    def handler_comment_product_submited(cls, notification, phonenumber):
        pattern = 'ar0prdkncw4dk9l'
        send_sms(phonenumber, pattern, {
            'user_name': notification.to_user.get_full_name()
        })

    @classmethod
    def handler_comment_product_accepted(cls, notification, phonenumber):
        pattern = 'ar0prdkncw4dk9l'
        send_sms(phonenumber, pattern, {
            'user_name': notification.to_user.get_full_name()
        })

    @classmethod
    def handler_comment_product_rejected(cls, notification, phonenumber):
        pattern = 'ar0prdkncw4dk9l'
        send_sms(phonenumber, pattern, {
            'user_name': notification.to_user.get_full_name()
        })

    @classmethod
    def handler_cart_status_updated(cls, notification, phonenumber):
        pattern = 'ar0prdkncw4dk9l'
        send_sms(phonenumber, pattern, {
            'user_name': notification.to_user.get_full_name()
        })

    @classmethod
    def handler_custom_product_status_rejected(cls, notification, phonenumber):
        pattern = 'ar0prdkncw4dk9l'
        send_sms(phonenumber, pattern, {
            'user_name': notification.to_user.get_full_name()
        })

    @classmethod
    def handler_password_changed_successfully(cls, notification, phonenumber):
        pattern = 'b2pw4o745dqs1hs'
        send_sms(phonenumber, pattern, {
            'notification_url': get_host_url(notification.get_link()),
            'user_name': notification.to_user.get_full_name()
        })

    @classmethod
    def handler_reset_password_code_sent(cls, notification, phonenumber):
        pattern = '0pcbtnsuif87g32'
        send_sms(phonenumber, pattern, {
            'code': notification.kwargs['code']
        })

    @classmethod
    def handler_user_account_activated(cls, notification, phonenumber):
        pattern = 'teouuo7p8oy9fd7'
        send_sms(phonenumber, pattern, {
            'user_name': notification.to_user.get_full_name()
        })

    @classmethod
    def handler_confirm_phonenumber_code_sent(cls, notification, phonenumber):
        pattern = 'hx4h9y3wpxzt5gs'
        send_sms(phonenumber, pattern, {
            'code': notification.kwargs['code']
        })

    @classmethod
    def handler_phonenumber_confirmed(cls, notification, phonenumber):
        pattern = 'sk44rthuce0y29o'
        send_sms(phonenumber, pattern, {
            'user_name': notification.to_user.get_full_name()
        })


NOTIFICATION_USER_HANDLERS = {
    'PAYMENT_SUCCESSFULLY_USER': NotificationUser.handler_payment_successfully_user,
    'NEW_PAYMENT_ADMIN': NotificationUser.handler_new_payment_admin,
    'CUSTOM_PRODUCT_ADDED_TO_CART': NotificationUser.handler_custom_product_added_to_cart,
    'COMMENT_SUBMITED_USER': NotificationUser.handler_comment_product_submited,
    'COMMENT_PRODUCT_ACCEPTED_USER': NotificationUser.handler_comment_product_accepted,
    'COMMENT_PRODUCT_REJECTED_USER': NotificationUser.handler_comment_product_rejected,
    'CART_STATUS_UPDATED': NotificationUser.handler_cart_status_updated,
    'CUSTOM_PRODUCT_STATUS_REJECTED': NotificationUser.handler_custom_product_status_rejected,

    'PASSWORD_CHANGED_SUCCESSFULLY': NotificationUser.handler_password_changed_successfully,
    'RESET_PASSWORD_CODE_SENT': NotificationUser.handler_reset_password_code_sent,
    'USER_ACCOUNT_ACTIVATED': NotificationUser.handler_user_account_activated,
    'CONFIRM_PHONENUMBER_CODE_SENT': NotificationUser.handler_confirm_phonenumber_code_sent,
    'PHONENUMBER_CONFIRMED': NotificationUser.handler_phonenumber_confirmed,
}
