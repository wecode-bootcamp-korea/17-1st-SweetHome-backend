from django.http            import JsonResponse
from django.views           import View
from django.db.models       import Count

from user.models    import User
from posting.models import (
        Posting,
        PostingSize,
        PostingHousing,
        PostingStyle,
        PostingSpace,
        PostingLike,
        PostingComment,
        PostingScrap
)

class PostingView(View):
    def get(self, request):
        postings        = Posting.objects.all()
        sort_request    = request.GET.get('sort', 'recent')
        postings        = postings.annotate(like_num=Count("postinglike"))
        postings        = postings.annotate(comment_num=Count("comment"))
        postings        = postings.annotate(scrap_num=Count("postingscrap"))
        
        sort_prefixes = {
                "like"      : "-like_num",
                "popular"   : "-comment_num",
                "scrap"     : "-scrap_num",
                "recent"    : "-created_at",
                "old"       : "created_at"
                }

        filter_prefixes = {
                'size_id'       : 'size_id__in',
                'housing_id'    : 'housing_id__in',
                'style_id'      : 'style_id__in',
                'space_id'      : 'space_id__in'
                }
        filter_set = {
                filter_prefixes.get(key) : value for (key, value) in dict(request.GET).items() 
                if filter_prefixes.get(key)
                }

        postings = postings.filter(**filter_set).order_by(sort_prefixes[sort_request])

        posting_list = [{
                "id"                        : posting.id,
                "card_user_image"           : posting.user.image_url,
                "card_user_name"            : posting.user.name,
                "card_user_introduction"    : posting.user.description,
                "card_image"                : posting.image_url,
                "card_content"              : posting.content,
                "comment_num"               : posting.comment.filter(posting_id=posting.id).count() if posting.comment.exists() else 0,
                "comment_user_image"        : posting.comment.first().user.image_url if posting.comment.exists() else None,
                "comment_user_name"         : posting.comment.first().user.name if posting.comment.exists() else None,
                "comment_content"           : posting.comment.first().content if posting.comment.exists() else None,
                "like_num"                  : posting.postinglike_set.filter(posting_id=posting.id).count() if posting.postinglike_set.exists() else 0,
                "scrap_num"                 : posting.postingscrap_set.filter(posting_id=posting.id).count() if posting.postingscrap_set.exists() else 0,
                "created_at"                : posting.created_at
                } for posting in postings
        ]
        return JsonResponse({'message' : posting_list}, status=200)

class CategoryView(View):
    def get(self, request):
        sortings    = [{"id" : 1, "name" : "역대인기순"}, {"id" : 2, "name" : "댓글많은순"}, {"id" : 3, "name" : "스크랩많은순"}, {"id" : 4, "name" : "최신순"}, {"id" : 5, "name" : "오래된순"}]
        
        category_condition = {
                "categories" : [
                    {
                        "id" : 1,
                        "categoryName" : "정렬",
                        "category" : [name for name in list(sortings)]
                        },
                    {
                        "id" : 2,
                        "categoryName" : "주거형태",
                        "category" : [name for name in list(PostingHousing.objects.values())]
                    },
                    {
                        "id" : 3,
                        "categoryName" : "공간",
                        "category" : [name for name in list(PostingSpace.objects.values())]
                    },
                    {
                        "id" : 4,
                        "categoryName" : "평수",
                        "category" : [name for name in list(PostingSize.objects.values())]
                    },
                    {
                        "id" : 5,
                        "categoryName" : "스타일",
                        "category" : [name for name in list(PostingStyle.objects.values())]
                    }]
                }
        return JsonResponse({'categories' : category_condition}, status=200)
