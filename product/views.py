import json

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q, Count

from product.models import Product, ProductReview, ReviewLike

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