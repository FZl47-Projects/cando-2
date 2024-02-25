
# get product images path
def product_images_path(instance, path):
    product = instance.product.title
    return f'images/products/{product}/{path}'
