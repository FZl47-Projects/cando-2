from apps.core.utils import random_str, get_time


def get_upload_src_product_attr_pic(instance, path):
    frmt = str(path).split('.')[-1]
    tm = get_time('%Y-%m-%d')
    return f'images/product-attr/{tm}/{random_str()}.{frmt}'


