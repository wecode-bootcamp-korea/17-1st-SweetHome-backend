from django.http      import JsonResponse
from django.views     import View
from django.db.models import Avg

from product.models import Product

class ProductView(View):
    def get(self, request):
        category        = request.GET.get('category', None)
        sub_category    = request.GET.get('subcategory', None)
        detail_category = request.GET.get('detailcategory', None)
        order           = request.GET.get('order', None)
        color           = request.GET.get('color', None)
        size            = request.GET.get('size', None)

        products = Product.objects.all()

        if category:
            products = Product.objects.filter(detail_category__sub_category__category=category)

        if sub_category:
            products = products.filter(detail_category__sub_category=sub_category)

        if detail_category:
            products = products.filter(detail_category=detail_category)

        if color:
            products = products.filter(productoption__color_id=color).distinct()

        if size:
            products = products.filter(productoption__size_id=size).distinct()

        product_list = [{
            'id'                  : product.id,
            'name'                : product.name,
            'discount_percentage' : int(product.discount_percentage),
            'discount_price'      : int(product.original_price) * (100 - int(product.discount_percentage)) // 100,
            'company'             : product.company.name,
            'image'               : product.productimage_set.first().image_url,
            'rate_average'        : round(product.productreview_set.aggregate(Avg('rate'))['rate__avg'], 1)\
                    if product.productreview_set.aggregate(Avg('rate'))['rate__avg'] else None,
            'review_count'        : product.productreview_set.count(),
            'is_free_delivery'    : True if product.delivery.fee.price == 0 else False,
            'is_on_sale'          : True if int(product.discount_percentage) != 0 else False,
            'created_at'          : product.created_at
            } for product in products
        ]

        if order == 'recent':
            product_list = sorted(product_list, key=lambda product: product['created_at'], reverse=True)

        if order == 'old':
            product_list = sorted(product_list, key=lambda product: product['created_at'])

        if order == 'min_price':
            product_list = sorted(product_list, key=lambda product: product['discount_price'])

        if order == 'max_price':
            product_list = sorted(product_list, key=lambda product: product['discount_price'], reverse=True)

        if order == 'review':
            product_list = sorted(product_list, key=lambda product: product['review_count'], reverse=True)

        return JsonResponse({'message': product_list}, status=200)
