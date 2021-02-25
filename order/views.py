import json

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q
from django.db.utils  import DataError

from user.models    import User
from user.utils     import login_decorator
from order.models   import Order, OrderStatus, OrderProduct
from product.models import Product

class OrderProductView(View):
    @login_decorator
    def get(self, request):
        try:
            user = request.user

            if not Order.objects.filter(Q(user=user)&Q(status=1)).exists():
                return JsonResponse({'message':'NO_PRODUCTS'}, status=200)
            order = Order.objects.get(Q(user=user)&Q(status=1))
            
            order_products  = order.orderproduct_set.all()

            results = [
            {
                "product_id"             : order_product.id, 
                "product_option_id"      : order_product.product_option.id,
                "product_name"           : order_product.product_option.product.name,
                "product_color"          : order_product.product_option.color.name,
                "product_size"           : order_product.product_option.size.name,
                "quantity"               : order_product.quantity,
                "product_original_price" : order_product.product_option.product.original_price,
                "product_image"          : order_product.product_option.product.productimage_set.all()[0].image_url,
                "product_price"          : order_product.product_option.product.original_price * (100 - product.discount_percentage) / 100,
                "product_company"        : order_product.product_option.product.company.name,
                "product_delivery_type"  : order_product.product_option.product.delivery.method.name,
                "product_delivery_fee"   : order_product.product_option.product.delivery.fee.price,
            } for order_product in order_products]
            
            return JsonResponse({'results':results}, status=200)

        except json.decoder.JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        
        except DataError:
            return JsonResponse({'message':'DATA_ERROR'}, status=400)

    @login_decorator
    def post(self, request):
        try:
            user = request.user

            data = json.loads(request.body)
            product_option_id = data['id']
            quantity = data['quantity']
            total_price = data['total_price']

            if product_option_id:
                order_product          = OrderProduct.objects.get(Q(product_option_id=product_option_id)&Q(order__status=1))
                order_product.quantity = quantity
                order_product.save()

                if not Order.objects.filter(Q(user=user)&Q(status=1)).exists():
                    return JsonResponse({'message':'NO_PRODUCTS'}, status=200)

                order           = Order.objects.get(Q(user=user)&Q(status=1))
                order_products  = order.orderproduct_set.all()

                results = [
                {
                    "product_id"             : order_product.id, 
                    "product_option_id"      : order_product.product_option.id,
                    "product_name"           : order_product.product_option.product.name,
                    "product_color"          : order_product.product_option.color.name,
                    "product_size"           : order_product.product_option.size.name,
                    "quantity"               : order_product.quantity,
                    "product_original_price" : order_product.product_option.product.original_price,
                    "product_image"          : order_product.product_option.product.productimage_set.all()[0].image_url,
                    "product_price"          : order_product.product_option.product.original_price * (100 - product.discount_percentage) / 100,
                    "product_company"        : order_product.product_option.product.company.name,
                    "product_delivery_type"  : order_product.product_option.product.delivery.method.name,
                    "product_delivery_fee"   : order_product.product_option.product.delivery.fee.price,
                } for order_product in order_products]

                return JsonResponse({'message':results}, status=200)

            order = Order.objects.get(Q(user=user)&Q(status=1))
            order.total_price = total_price
            order.save()

            return JsonResponse({'message':'SUCCESS'}, status=200)

        except json.decoder.JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)