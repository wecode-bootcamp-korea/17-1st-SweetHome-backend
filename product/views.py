from django.http      import JsonResponse
from django.views     import View
from django.db.models import Avg, Count

from product.models import Product

DISCOUNT_PROUDCTS_COUNT = 5

class ProductView(View):
    def get(self, request):
        order_condition    = request.GET.get('order', None)
        top_list_condition = request.GET.get('top', None)

        filter_prefixes = {
            'category'       : 'detail_category__sub_category__category__in',
            'subcategory'    : 'detail_category__sub_category__in',
            'detailcategory' : 'detail_category__in',
            'color'          : 'productoption__color__in',
            'size'           : 'productoption__size__in'
        }

        filter_set = {
            filter_prefixes.get(key) : value for (key, value) in dict(request.GET).items() if filter_prefixes.get(key)
        }
        
        products = Product.objects.filter(**filter_set).distinct()
        
        order_by_time  = {'recent' : 'created_at', 'old' : '-created_at'}
        order_by_price = {'min_price' : 'discount_price', 'max_price' : '-discount_price'}

        if order_condition in order_by_time:
            products = products.order_by(order_by_time[order_condition])

        if order_condition in order_by_price:
            products = products.extra(
                    select={'discount_price' : 'original_price * (100 - discount_percentage) / 100'}).order_by(
                    order_by_price[order_condition])

        if order_condition == 'review':
            products = products.annotate(review_count=Count('productreview')).order_by('-review_count')
                
        if top_list_condition == 'discount': 
            products = Product.objects.all().order_by('-discount_percentage')[:DISCOUNT_PROUDCTS_COUNT]

        products_list = [{
            'id'                  : product.id,
            'name'                : product.name,
            'discount_percentage' : int(product.discount_percentage),
            'discount_price'      : int(product.original_price) * (100 - int(product.discount_percentage)) // 100,
            'company'             : product.company.name,
            'image'               : product.productimage_set.first().image_url,
            'rate_average'        : round(product.productreview_set.aggregate(Avg('rate'))['rate__avg'], 1)\
                    if product.productreview_set.aggregate(Avg('rate'))['rate__avg'] else 0,
            'review_count'        : product.productreview_set.count(),
            'is_free_delivery'    : product.delivery.fee.price == 0,
            'is_on_sale'          : not (int(product.discount_percentage) == 0),
            } for product in products
        ]

        products_count = products.count()

        return JsonResponse({'products' : products_list, 'count' : products_count}, status=200)
