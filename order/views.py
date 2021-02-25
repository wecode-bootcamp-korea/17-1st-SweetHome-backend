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
            product_tuple = [(i, i.product_option, i.product_option.product) for i in order_products]

            results = [
            {
                "product_id"             : product.id, 
                "product_option_id"      : product_option.id,
                "product_name"           : product.name,
                "product_color"          : product_option.color.name,
                "product_size"           : product_option.size.name,
                "quantity"               : order_product.quantity,
                "product_original_price" : product.original_price,
                "product_image"          : product.productimage_set.all()[0].image_url,
                "product_price"          : product.original_price * (100 - product.discount_percentage) / 100,
                "product_company"        : product.company.name,
                "product_delivery_type"  : product.delivery.method.name,
                "product_delivery_fee"   : product.delivery.fee.price,
            } for (order_product, product_option, product) in product_tuple]
            
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
                product_tuple   = [(i, i.product_option, i.product_option.product) for i in order_products]

                results = [
                {
                    "product_id"             : product.id, 
                    "product_option_id"      : product_option.id,
                    "product_name"           : product.name,
                    "product_color"          : product_option.color.name,
                    "product_size"           : product_option.size.name,
                    "quantity"               : order_product.quantity,
                    "product_original_price" : product.original_price,
                    "product_image"          : product.productimage_set.all()[0].image_url,
                    "product_price"          : product.original_price * (100 - product.discount_percentage) / 100,
                    "product_company"        : product.company.name,
                    "product_delivery_type"  : product.delivery.method.name,
                    "product_delivery_fee"   : product.delivery.fee.price,
                } for (order_product, product_option, product) in product_tuple]

                return JsonResponse({'message':results}, status=200)

            order = Order.objects.get(Q(user=user)&Q(status=1))
            order.total_price = total_price
            order.save()

            return JsonResponse({'message':'SUCCESS'}, status=200)

        except json.decoder.JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)