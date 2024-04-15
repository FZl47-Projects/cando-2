import requests
import json
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.conf import settings
from django.shortcuts import redirect

from apps.core.utils import log_event

try:
    ZARINPAL_CONFIG = settings.GATEWAYS_BANK['ZARINPAL']
except KeyError:
    raise ValueError('You should set zarinpal gateways config to use it')


class Zarinpal:
    is_success = False
    SANDBOX = ZARINPAL_CONFIG['SANDBOX']

    def get_api_startpay(self):
        if self.SANDBOX:
            return 'https://sandbox.zarinpal.com/pg/StartPay/{}/ZarinGate'
        return 'https://www.zarinpal.com/pg/StartPay/{}/ZarinGate'

    def get_api_verify(self):
        if self.SANDBOX:
            return 'https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentVerification.json'
        return 'https://www.zarinpal.com/pg/rest/WebGate/PaymentVerification.json'

    def get_api_request(self):
        if self.SANDBOX:
            return 'https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentRequest.json'
        return 'https://www.zarinpal.com/pg/rest/WebGate/PaymentRequest.json'

    def start_transaction(self, request, amount, callback_url, description=None, phonenumber=None):
        self.request = request
        data = {
            "MerchantID": ZARINPAL_CONFIG['MERCHANT_CODE'],
            "Amount": str(amount),
            "Description": description or ZARINPAL_CONFIG['DESCRIPTION'],
            "Mobile": phonenumber,
            "CallbackURL": str(callback_url),
        }
        data = json.dumps(data)
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}
        try:
            response = requests.post(self.get_api_request(), data=data, headers=headers, timeout=20)
            if response.status_code != 200:
                msg_err = 'Bad Request Please Notify Support'
                messages.error(request, _(msg_err))
                log_event(msg_err, 'CRITICAL')
                return False
            response = response.json()
            if response['Status'] != 100:
                msg_err = 'Request Status Is Not Valid'
                messages.error(request, _(msg_err))
                log_event(msg_err, 'ERROR')
                return False
            self.response = response
            self._authority = response['Authority']
            self.is_success = True
            return True

        except requests.exceptions.Timeout:
            msg_err = 'Connection Timeout'
            messages.error(request, _(msg_err))
            log_event(msg_err, 'WARNING', exc_info=True)
            return False
        except requests.exceptions.ConnectionError:
            msg_err = 'There Is Some Problem In Connection Please Try Again'
            messages.error(request, _(msg_err))
            log_event(msg_err, 'WARNING', exc_info=True)
            return False

    def redirect_to_gateway(self):
        return redirect(self.get_api_startpay().format(self._authority))

    def verify_transaction(self, request, amount):
        authority = request.GET.get('Authority')
        if not authority:
            msg_err = 'Request Is Invalid'
            messages.error(request, _(msg_err))
            log_event(msg_err, 'WARNING')
            return False
        data = {
            "MerchantID": ZARINPAL_CONFIG['MERCHANT_CODE'],
            "Amount": str(amount),
            "Authority": authority,
        }
        data = json.dumps(data)
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}
        response = requests.post(self.get_api_verify(), data=data, headers=headers)
        if response.status_code != 200:
            msg_err = 'Bad Request Please Notify Support'
            messages.error(request, _(msg_err))
            log_event(msg_err, 'CRITICAL')
            return False
        response = response.json()
        if not response['Status'] in [100, 101]:
            msg_err = 'Request Status Is Not Valid'
            messages.error(request, _(msg_err))
            log_event(msg_err, 'ERROR')
            return False
        self.response = response
        return True
