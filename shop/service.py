import base64
import os

import pdfkit
from decouple import config
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django_filters import rest_framework as filters

from shop.models import Product, Manufacturer
from shop_server.settings import BASE_DIR


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class ChartFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class ProductFilter(filters.FilterSet):
    category = ChartFilterInFilter(field_name='category', lookup_expr='in')

    class Meta:
        model = Product
        fields = ['category']


def get_img_file_as_base64():
    img_manufacturer = Manufacturer.objects.get(title='Pfunt').img_manufacturer
    url = os.path.join(BASE_DIR, 'media', str(img_manufacturer))
    with open(url, 'rb') as img_file:
        return base64.b64encode(img_file.read()).decode()


def create_pdf(order, order_items, tax, ):
    img = get_img_file_as_base64()
    html_pdf = render_to_string(
        'order_to_pdf.html',
        {
            'order': order,
            'order_items': order_items,
            'tax': tax,
            'img': img
        })
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config1 = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    path_pdf = settings.MEDIA_ROOT + f'\invoices\Rechnung №{order.id}.pdf'
    pdfkit.from_string(html_pdf, path_pdf, configuration=config1, options={"enable-local-file-access": ""})
    order.invoice = f'invoices/Rechnung №{order.id}.pdf'
    pdf = pdfkit.from_string(html_pdf, False, configuration=config1, options={"enable-local-file-access": ""})
    return pdf


def send_email_with_attach(order, order_items, tax, ):

    html_order = render_to_string(
        'order.html',
        {
            'order': order,
            'order_items': order_items,
            'tax': tax,
        }
    )

    order_message = EmailMultiAlternatives(
        subject=f'Bestellung №{order.id} ist am {order.date_created.strftime("%d.%m.%Y")} angekommen',
        body=f'Bestellung №{order.id}',
        from_email=config('EMAIL_USER'),
        to=[config('EMAIL_USER'), order.email]
    )
    order_message.attach_alternative(html_order, 'text/html')
    order_message.attach(f'Rechnung №{order.id}', create_pdf(order, order_items, tax, ), 'application/pdf')
    order_message.send()
