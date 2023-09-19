from django_filters import rest_framework as filters

from shop.models import Product


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
