import json
import bcrypt
import jwt

from django.views import View
from django.http  import JsonResponse

from my_settings  import SECRET_KEY, ALGORITHM
from .utils       import login_decorator
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


class SigninView(View):
    def post(self, request):
        try: 
            data     = json.loads(request.body)
            email    = data['email']
            password = data['password']

            if not User.objects.filter(email = email).exists():
                if not User.objects.filter(password = password).exists():
                    return JsonResponse({'mesage' : 'INVALID_USER'}, status = 401)

            user = User.objects.get(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                token = jwt.encode({'user_id': user.id}, SECRET_KEY, ALGORITHM)
                return JsonResponse({'message': 'SUCCESS', 'access_token': token}, status=201)
            return JsonResponse({'message': 'INVALID_PASSWORD'}, status=401)
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)


