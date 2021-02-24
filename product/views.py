import json

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q, Count

from product.models import Product, ProductReview, ReviewLike
from user.models    import User

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
    # 상품 리뷰에 도움이 됐다를 표시하면 like 표시
    def post(self, request, product_id):
        try:
            data     = json.loads(request.body)
            review_id = data.get('review_id')

            # user는 login_decorator로 불러온다.
            email    = data.get('email')
            password = data.get('password')

            if not email:
                return JsonResponse({'message':'NO_EMAIL_ERROR'}, status=400)

            if not User.objects.filter(email=email).exists():
                return JsonResponse({'message':'INVALID_USER'}, status=401)

            user = User.objects.get(email=email)

            if ProductReview.objects.filter(id=review_id).exists():
                product_review = ProductReview.objects.get(id=review_id)
            else:
                return JsonResponse({'message':'INVALID_REVIEW'}, status=401)
            
            if product_review.user == user:
                return JsonResponse({'message':'CANNOT_LIKE_YOUR_REVIEW'}, status=401)
            
            if ReviewLike.objects.filter(review=product_review, user=user).exists():
                ReviewLike.objects.filter(review=product_review, user=user).delete()
            else:
                ReviewLike.objects.create(review=product_review, user=user)
        
            return JsonResponse({'message':'SUCCESS'}, status=200)

        except json.decoder.JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        
        except Product.DoesNotExist:
            return JsonResponse({'message':'PRODUCT_DOES_NOT_EXIST'}, status=400)