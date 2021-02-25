import json

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Avg, Count, Q

from user.models    import User
from user.utils     import login_decorator
from product.models import (
  Product, 
  ProductReview, 
  ReviewLike,
  ProductOption,
  ProductColor,
  ProductSize,
  Category
)
from order.models   import OrderProduct, Order, OrderStatus
from user.utils     import login_decorator

DISCOUNT_PROUDCTS_COUNT = 5

class CategoryView(View):
    def get(self, request):
        category_list = [{
            'id': category.id,
            'name': category.name,
            'sub_category': [{
                'id': sub_category.id,
                'name': sub_category.name,
                'detail_category' : [{
                    'id': detail_category.id,
                    'name': detail_category.name
                } for detail_category in sub_category.detailcategory_set.all()]
            } for sub_category in category.subcategory_set.all()]
        } for category in Category.objects.all().order_by('id')]
        return JsonResponse({'categories': category_list}, status=200)

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

class ProductCartView(View):
    @login_decorator
    def post(self, request):
        try:
            user = request.user

            if not Product.objects.filter(id=product_id).exists():
                return JsonResponse({'message':'INVALID_PRODUCT'}, status=404)
            
            data     = json.loads(request.body)
            color    = ProductColor.objects.get(name=data['color'])
            size     = ProductSize.objects.get(name=data['size'])
            quantity = int(data['quantity'])
            product  = Product.objects.get(id=data['id'])
            
            if not ProductOption.objects.filter(
                product=Product.objects.get(id=product_id),color=color, size=size
            ).exists():
                return JsonResponse({'message':'INVALID_PRODUCT_OPTION'}, status=404)

            product_option = ProductOption.objects.get(
                product=Product.objects.get(id=product_id),color=color, size=size
            )
            order = Order.objects.create(user=user, status_id=1)

            if OrderProduct.objects.filter(order=order, product_option=product_option, order__status=1).exists(): 
                order_products = OrderProduct.objects.filter(order=order, product_option=product_option)
                for order_product in order_products:
                    order_product.quantity+=quantity
                    order_product.save()
            else:
                OrderProduct.objects.create(
                    order=order, product_option=product_option, quantity=quantity
                )
            
            return JsonResponse({'message':'SUCCESS'}, status=201)

        except json.decoder.JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
          
class ProductDetailView(View):
    def get(self, request, product_id):
        if not Product.objects.filter(id=product_id).exists():
            return JsonResponse({'message':'INVALID_PRODUCT'}, status=404)

        product = Product.objects.get(id=product_id)

        product_detail = {
            'id'                  : product.id,
            'name'                : product.name,
            'original_price'      : int(product.original_price),
            'discount_percentage' : int(product.discount_percentage),
            'discount_price'      : int(product.original_price) * (100 - int(product.discount_percentage)) // 100,
            'company'             : product.company.name,
            'image'               : [i.image_url for i in product.productimage_set.all()],
            'rate_average'        : round(product.productreview_set.aggregate(Avg('rate'))['rate__avg'], 1)\
                if product.productreview_set.aggregate(Avg('rate'))['rate__avg'] else 0,
            'review_count'        : product.productreview_set.count(),
            'delivery_type'       : product.delivery.method.name,
            'delivery_period'     : product.delivery.period.day,
            'delivery_fee'        : product.delivery.fee.price,
            'is_free_delivery'    : product.delivery.fee.price == 0,
            'is_on_sale'          : not (int(product.discount_percentage) == 0),
            'size'                : list(set([i.size.name for i in product.productoption_set.all()])),
            'color'               : list(set([i.color.name for i in product.productoption_set.all()])),
        }
        return JsonResponse({'product': product_detail}, status=200)

class ProductReviewView(View):
    def get(self, request, product_id):
        try:
            product   = Product.objects.get(id=product_id)
            order     = request.GET.get('order', 'recent')
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

class ReviewLikeView(View):
    @login_decorator
    def post(self, request, product_id):
        try:
            data     = json.loads(request.body)
            review_id = data.get('review_id')

            user = request.user

            if not ProductReview.objects.filter(id=review_id).exists():
                return JsonResponse({'message':'INVALID_REVIEW'}, status=401)

            product_review = ProductReview.objects.get(id=review_id)
            
            if user.productreview_set.filter(id=review_id).exists():
                return JsonResponse({'message':'CANNOT_LIKE_YOUR_REVIEW'}, status=401)
            
            review_like, created = ReviewLike.objects.get_or_create(review=product_review, user=user)

            if not created:
                review_like.delete()

            return JsonResponse({'message':'SUCCESS'}, status=200)

        except json.decoder.JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        
        except Product.DoesNotExist:
            return JsonResponse({'message':'PRODUCT_DOES_NOT_EXIST'}, status=400)
