import json

from django.http      import JsonResponse
from django.views     import View
from django.db.utils  import DataError

from user.models  import User
from order.models import Order, OrderProduct

class OrderView(View):
    def post(self, request):
        try:
            data                    = json.loads(request.body)
            # user id를 불러올 때 어떤 형식으로 불러오는가
            user_id                 = data['user_id']
            sender_name             = data['sender_name']
            sender_email            = data['sender_email']
            sender_phone_number     = data['sender_phone_number']
            recipient_name          = data['recipient_name']
            recipient_phone_number  = data['recipient_phone_number']
            recipient_address       = data['recipient_address']
            total_amount            = data['total_amount']

            user = User.objects.create(id=user_id)
            Order.objects.create(
                user=user,
                sender_name=sender_name,
                sender_email=sender_email,
                sender_phone_number=sender_phone_number,
                recipient_name=recipient_name,
                recipient_phone_number=recipient_phone_number,
                recipient_address=recipient_address,
                total_amount=total_amount
            )

            return JsonResponse({'message':'SUCCESS'}, status=200)

        except json.decoder.JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        
        except DataError:
            return JsonResponse({'message':'DATA_ERROR'}, status=400)

class OrderProductView(View):
    def post(self, request):
        try:
            data           = json.loads(request.body)
            # product_option id를 불러올 때 어떤 형식으로 불러오는가. 오브젝트?

            product_option = data['product_option_id']
            quantity       = data['quantity']
            order          = data['order_id']

            return JsonResponse({'message':'SUCCESS'}, status=200)

        except json.decoder.JSONDecodeError:
            return JsonResponse({'message':'JSON_DECODE_ERROR'}, status=400)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        
        except DataError:
            return JsonResponse({'message':'DATA_ERROR'}, status=400)


    