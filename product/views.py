import json

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Avg, Count, Q

from product.models import (
  Product, 
  ProductReview, 
  ReviewLike,
  ProductOption,
  ProductColor,
  ProductSize,
)
from order.models   import OrderProduct, Order, OrderStatus

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

class ProductDetailView(View):
    @login_decorator
    def post(self, request, product_id):
        try:
            if not Product.objects.filter(id=product_id).exists():
                return JsonResponse({'message':'INVALID_PRODUCT'}, status=404)

            product = Product.objects.get(id=product_id)
            
            data     = json.loads(request.body)
            color    = ProductColor.objects.get(name=data['color'])
            size     = ProductSize.objects.get(name=data['size'])
            quantity = int(data['quantity'])

            user = request.user

            product_option = ProductOption.objects.update_or_create(
                product=Product.objects.get(id=product_id),color=color, size=size
            )[0]
            order = Order.objects.update_or_create(user=user, status=OrderStatus.objects.get(id=1))[0]

            if OrderProduct.objects.filter(order=order, product_option=product_option, order__status=1).exists(): 
                order_products = OrderProduct.objects.filter(order=order, product_option=product_option)
                for order_product in order_products:
                    order_product.quantity+=quantity
                    order_product.save()
            else:
                OrderProduct.objects.create(
                    order=order, product_option=product_option, quantity=quantity
                )

            return JsonResponse({'message':'SUCCESS'}, status=200)

        except json.decoder.JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

class ProductReviewView(View):
    def get(self, request, product_id):
        try:
            product   = Product.objects.get(id=product_id)
            order     = request.GET.get('order', None)
            rate_list = request.GET.getlist('rate', None)
            like      = request.GET.get('like', None)

            if rate_list:
                q = Q()
                for rate in rate_list:
                    q.add(Q(rate=rate), q.OR)
                q.add(Q(product=product), q.AND)
            else:
                q = Q(product=product)

            order_dict = {
                'old'   :'created_at',
                'recent':'-created_at',
                'like'  :'-review_like',
            }

            if order in order_dict:
                product_reviews = ProductReview.objects.filter(q)\
                    .annotate(review_like=Count('reviewlike')).order_by(order_dict[order])
            
            results = [{
                        "review_id"        : product_review.id,
                        "review_content"   : product_review.content,
                        "review_image"     : product_review.image_url,
                        "review_rate"      : product_review.rate,
                        "product_name"     : product.name,
                        "day"              : str(product_review.created_at).split(" ")[0],
                        "review_user_name" : product_review.user.name,
                        "review_like"      : product_review.review_like,
                    } for product_review in product_reviews]

            return JsonResponse({'results':results}, status=200)

        except json.decoder.JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        
        except Product.DoesNotExist:
            return JsonResponse({'message':'PRODUCT_DOES_NOT_EXIST'}, status=400)