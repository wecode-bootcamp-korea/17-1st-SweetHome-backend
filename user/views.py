import json
import bcrypt

from django.views import View
from django.http  import JsonResponse

from my_settings  import SECRET_KEY
from .models      import User

MINIMUM_PASSWORD_LENGTH = 8
MINIMUM_NAME_LENGTH = 2
MAXIMUN_NAME_LENGTH = 15


class SignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email    = data['email']
            password = data['password']                                
            name     = data['name']

            if len(password) < MINIMUM_PASSWORD_LENGTH:
                return JsonResponse({'message' : 'INVALID_PASSWORD'}, status = 400)

            if not email:
                return JsonResponse({'message' : 'INVALID_EMAIL'}, status = 400)

            if len(name) < MINIMUM_NAME_LENGTH and len(name) > MAXIMUN_NAME_LENGTH:
                return JsonResponse({'message' : 'INVALID_NAME'}, status = 400)

            if User.objects.filter(name = name).exists():
                return JsonResponse({'message' : 'USER_ALREADY_EXISTS'}, status = 400)

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
                email    = email,
                password = hashed_password,
                name     = name,
            )
            return JsonResponse({'message' : 'SUCCESS'}, status = 201)
                
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

