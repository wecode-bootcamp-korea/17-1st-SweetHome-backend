import json

from django.views import View
from django.http  import JsonResponse

from user.utils  import login_decorator
from .models import PostingScrap


class PostingScrapView(View):
    @login_decorator
    def post(self, request):
        data       = json.loads(request.body)
        user_id    = request.user
        posting_id = data['posting_id']

        if PostingScrap.objects.filter(user=user_id, posting_id=posting_id).exists():
            posting_scrap = PostingScrap.objects.filter(user=user_id, posting_id=posting_id)
            posting_scrap.delete()
            return JsonResponse({'message' : 'SUCCESS'}, status=204)

        PostingScrap.objects.create(user=user_id, posting_id=posting_id)
        return JsonResponse({'message' : 'SUCCESS'}, status=201)
