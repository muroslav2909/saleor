from django.conf import settings
from django.utils.encoding import smart_text

from django_prices_vatlayer.utils import get_tax_for_country


def get_attributes_display_map(obj, attributes):
    display_map = {}
    for attribute in attributes:
        value = obj.attributes.get(smart_text(attribute.pk))
        if value:
            choices = {smart_text(a.pk): a for a in attribute.values.all()}
            choice_obj = choices.get(value)
            if choice_obj:
                display_map[attribute.pk] = choice_obj
            else:
                display_map[attribute.pk] = value
    return display_map


def get_price_with_vat(product, price, country):
    if country and settings.VATLAYER_ACCESS_KEY:
        rate_name = product.product_class.vat_rate_type
        vat = get_tax_for_country(country, rate_name)
        if vat:
            price = vat.apply(price).quantize('0.01')
    return price
