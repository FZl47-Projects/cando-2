from apps.core.utils import send_sms, get_host_url


class NotificationUser:

    @classmethod
    def handler_custom_notification(cls, notification, phonenumber):
        pattern = '#'  # TODO: should be completed
        send_sms(phonenumber, pattern, {
            'notification_url': get_host_url(notification.get_link()),
            'user_name': notification.to_user.get_full_name()
        })

    @classmethod
    def handler_payment_successfully_user(cls, notification, phonenumber):
        pattern = '9q5zmq9tggh5c22'
        print(notification.get_link())
        send_sms(phonenumber, pattern, {
            'notification_url': get_host_url(notification.get_link()),
            'user_name': notification.to_user.get_full_name()
        })

    @classmethod
    def handler_new_payment_admin(cls, notification, phonenumber):
        pattern = 'nxips8jcalga8rl'
        send_sms(phonenumber, pattern, {
            'notification_url': get_host_url(notification.get_link()),
        })

    @classmethod
    def handler_custom_product_created(cls, notification, phonenumber):
        pattern = 'jh01r9a6y1pl234'
        send_sms(phonenumber, pattern, {
            'custom_product_link': notification.kwargs.get('custom_product_link')
        })

    @classmethod
    def handler_custom_product_added_to_cart(cls, notification, phonenumber):
        pattern = 'kzc10z9fnrpeef2'
        send_sms(phonenumber, pattern, {
            'notification_url': get_host_url(notification.get_link()),
            'user_name': notification.to_user.get_full_name()
        })

    @classmethod
    def handler_comment_product_submited(cls, notification, phonenumber):
        pattern = 'fyizmk3f11k7dpk'
        send_sms(phonenumber, pattern, {
            'user_name': notification.to_user.get_full_name()
        })

    @classmethod
    def handler_comment_product_accepted(cls, notification, phonenumber):
        pattern = 'o9fz31lv7qm7tf0'
        send_sms(phonenumber, pattern, {
            'user_name': notification.to_user.get_full_name()
        })

    @classmethod
    def handler_comment_product_rejected(cls, notification, phonenumber):
        pattern = 'nh47tl15dwdyni0'
        send_sms(phonenumber, pattern, {
            'notification_url': get_host_url(notification.get_link()),
            'user_name': notification.to_user.get_full_name()
        })

    @classmethod
    def handler_cart_status_updated(cls, notification, phonenumber):
        pattern = '9he7dgomq5k4qek'
        send_sms(phonenumber, pattern, {
            'notification_url': get_host_url(notification.get_link()),
            'status': notification.kwargs.get('status'),
            'user_name': notification.to_user.get_full_name()
        })

    @classmethod
    def handler_custom_product_status_rejected(cls, notification, phonenumber):
        pattern = '1sgmr9tmnouex9b'
        send_sms(phonenumber, pattern, {
            'notification_url': get_host_url(notification.get_link()),
            'user_name': notification.to_user.get_full_name()
        })

    @classmethod
    def handler_password_changed_successfully(cls, notification, phonenumber):
        pattern = '89wqp3zm71mve38'
        send_sms(phonenumber, pattern, {
            'notification_url': get_host_url(notification.get_link()),
            'user_name': notification.to_user.get_full_name()
        })

    @classmethod
    def handler_reset_password_code_sent(cls, notification, phonenumber):
        pattern = 'o0kf9qnplwqzjtz'
        send_sms(phonenumber, pattern, {
            'code': notification.kwargs['code']
        })

    @classmethod
    def handler_user_account_activated(cls, notification, phonenumber):
        pattern = 'iwcyqy0kq039hqo'
        send_sms(phonenumber, pattern, {
            'user_name': notification.to_user.get_full_name()
        })

    @classmethod
    def handler_confirm_phonenumber_code_sent(cls, notification, phonenumber):
        pattern = 'lin32i5ugdfu371'
        send_sms(phonenumber, pattern, {
            'code': notification.kwargs['code']
        })

    @classmethod
    def handler_phonenumber_confirmed(cls, notification, phonenumber):
        pattern = 'l31cuo3po9fpmmi'
        send_sms(phonenumber, pattern, {
            'user_name': notification.to_user.get_full_name()
        })


NOTIFICATION_USER_HANDLERS = {
    'CUSTOM_NOTIFICATION': NotificationUser.handler_custom_notification,
    'PAYMENT_SUCCESSFULLY_USER': NotificationUser.handler_payment_successfully_user,
    'NEW_PAYMENT_ADMIN': NotificationUser.handler_new_payment_admin,
    'CUSTOM_PRODUCT_CREATED': NotificationUser.handler_custom_product_created,
    'CUSTOM_PRODUCT_ADDED_TO_CART': NotificationUser.handler_custom_product_added_to_cart,
    'CUSTOM_PRODUCT_STATUS_REJECTED': NotificationUser.handler_custom_product_status_rejected,
    'COMMENT_SUBMITED_USER': NotificationUser.handler_comment_product_submited,
    'COMMENT_PRODUCT_ACCEPTED_USER': NotificationUser.handler_comment_product_accepted,
    'COMMENT_PRODUCT_REJECTED_USER': NotificationUser.handler_comment_product_rejected,
    'CART_STATUS_UPDATED': NotificationUser.handler_cart_status_updated,
    'PASSWORD_CHANGED_SUCCESSFULLY': NotificationUser.handler_password_changed_successfully,
    'RESET_PASSWORD_CODE_SENT': NotificationUser.handler_reset_password_code_sent,
    'USER_ACCOUNT_ACTIVATED': NotificationUser.handler_user_account_activated,
    'CONFIRM_PHONENUMBER_CODE_SENT': NotificationUser.handler_confirm_phonenumber_code_sent,
    'PHONENUMBER_CONFIRMED': NotificationUser.handler_phonenumber_confirmed,
}
