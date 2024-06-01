import requests
import json
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.conf import settings
from orders.models import Order
from django.contrib import messages
from django.http import HttpResponse


# def payment_process(request):
#     """get order id from session """
#     order_id = request.session.get('order_id')
#     order = get_object_or_404(Order, id=order_id)
#
#     toma_total_price = order.get_total_price()
#     rial_total_price = toma_total_price * 10
#     zarinpal_request_url = 'https://api.zarinpal.com/pg/v4/payment/request.json'
#
#     request_header = {
#         'accept': 'application/json',
#         'content-type': 'application/json',
#
#     }
#
#     request_data = {'merchant_id': settings.ZARINPAL_MERCHANT_ID,
#                     'amount': rial_total_price,
#                     'description': f'#{order.id}: {order.user.first_name} {order.user.last_name}',
#                     'callback_url': request.build_absolute_uri(reverse('product-list'))
#                     }
#
#     res = requests.post(url=zarinpal_request_url, data=json.dumps(request_data), headers=request_header)
#
#     data = res.json()['data']
#     authority = data['Authority']
#     order.zarinpal_authority = authority
#     order.save()
#
#     if 'errors' not in data or len(res.json()['errors']) == 0:
#         return redirect(f'https://www.zarinpal.com/pg/StartPay/{authority}'.format(authority=authority))
#     else:
#         return HttpResponse('Error form zarinpal')


def payment_callback(request):
    payment_authority = request.GET.get('Authorization')
    payment_status = request.GET.get('Status')

    order = get_object_or_404(Order, zarinpal_authority=payment_authority)

    toma_total_price = order.get_total_price()
    rial_total_price = toma_total_price * 10

    if payment_status == 'OK':
        request_header = {
            'accept': 'application/json',
            'content-type': 'application/json',

        }

        request_data = {'merchant_id': settings.ZARINPAL_MERCHANT_ID,
                        'amount': rial_total_price,
                        'authority': payment_authority,
                        }

        res = requests.post(url='https://api.zarinpal.com/pg/v4/payment/verify.json',
                                data=json.dumps(request_data),
                                headers=request_header
                            )

        if 'data' in res.json() and ('errors' not in res.json()['data'] or len(res.json()['data']['errors']) == 0):
            data = res.json()['data']
            payment_code = data['code']

            if payment_code == 100:
                order.is_paid = True
                order.ref_id = data['ref_id']
                order.zarinpal_data = data
                order.save()
                return HttpResponse('its ok')

            elif payment_code == 101:
                return HttpResponse('its ok already paid')
            else:
                error_code = res.json()['errors']['code']
                error_message = res.json()['errors']['message']
                return HttpResponse(f'not ok payment{error_code} {error_message}')


def payment_process_sandbox(request):
    """get order id from session """
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)

    toma_total_price = order.get_total_price()
    rial_total_price = toma_total_price * 10
    zarinpal_request_url = 'https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentRequest.json'

    request_header = {
        'accept': 'application/json',
        'content-type': 'application/json',

    }

    request_data = {'MerchantID': 'adadadadadadadadadadadadadadadadadad',
                    'Amount': rial_total_price,
                    'Description': f'#{order.id}: {order.user.first_name} {order.user.last_name}',
                    'CallbackURL': request.build_absolute_uri(reverse('payment:payment_callback'))
                    }

    res = requests.post(url=zarinpal_request_url, data=json.dumps(request_data), headers=request_header)

    data = res.json()

    authority = data['Authority']
    order.zarinpal_authority = authority
    order.save()

    if 'errors' not in data or len(res.json()['errors']) == 0:
        return redirect(f'https://sandbox.zarinpal.com/pg/StartPay/{authority}'.format(authority=authority))
    else:
        return HttpResponse('Error form zarinpal')


def payment_callback_sandbox(request):
    payment_authority = request.GET.get('Authority')
    payment_status = request.GET.get('Status')

    order = get_object_or_404(Order, zarinpal_authority=payment_authority)

    toma_total_price = order.get_total_price()
    rial_total_price = toma_total_price * 10

    if payment_status == 'OK':
        request_header = {
            'accept': 'application/json',
            'content-type': 'application/json',

        }

        request_data = {'MerchantID': 'adadadadadadadadadadadadadadadadadad',
                        'Amount': rial_total_price,
                        'Authority': payment_authority,
                        }

        res = requests.post(url='https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentVerification.json',
                            data=json.dumps(request_data), headers=request_header)

        if 'errors' not in res.json():
            data = res.json()
            payment_code = data['Status']

            if payment_code == 100:
                order.is_paid = True
                order.ref_if = data['RefID']
                order.zarinpal_data = data
                order.save()
                return render(request, template_name='payment/payment_ok.html')

            elif payment_code == 101:
                return render(request, 'payment/already.html')
            else:
                error_code = res.json()['errors']['code']
                error_message = res.json()['errors']['message']
                return HttpResponse(f'payment error{error_message} {error_code}')

    else:
        return HttpResponse('errors not valid')
