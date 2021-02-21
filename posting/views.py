from django.http            import JsonResponse
from django.views           import View

from user.models    import User
from posting.models import Posting

class PostingView(View):
    def get(self, request):
        postings        = Posting.objects.all()
        posting_list    = [{
            "id"                        : posting.id,
            "card_user_image"           : posting.user.imgage_url,
            "card_user_name"            : posting.user.name,
            "card_user_introduction"    : posting.user.description,
            "card_image"                : posting.image_url,
            "card_content"              : posting.content,
            "comment_user_image"        : posting.postingcomment_set.first().user.image_url if posting.postingcomment_set.exists() else None,
            "comment_user_name"         : posting.postingcomment_set.first().user.name if posting.postingcomment_set.exists() else None,
            "comment_content"           : posting.postingcomment_set.first().content if posting.postingcomment_set.exists() else None,
            } for posting in postings
        ]
        return JsonResponse({'message' : posting_list}, status=200)
