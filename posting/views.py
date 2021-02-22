from django.http            import JsonResponse
from django.views           import View

from user.models    import User
from posting.models import (
        Posting,
        PostingSize,
        PostingHousing,
        PostingStyle,
        PostingSpace,
        PostingLike,
        PostingComment
)

class PostingView(View):
    def get(self, request):
        sort = request.GET.get('sort', None)
        f_size = request.GET.get('size_id', None)
        f_housing = request.GET.get('housing_id', None)
        f_style = request.GET.get('style_id', None)
        f_space = request.GET.get('space_id', None)

        postings = Posting.objects.all()

        if f_size:
            postings = postings.filter(size_id=f_size)
        if f_housing:
            postings = postings.filter(housing_id=f_housing)
        if f_style:
            postings = postings.filter(style_id=f_style)
        if f_space:
            postings = postings.filter(space_id=f_space)

        posting_list    = [{
                "id"                        : posting.id,
                "card_user_image"           : posting.user.image_url,
                "card_user_name"            : posting.user.name,
                "card_user_introduction"    : posting.user.description,
                "card_image"                : posting.image_url,
                "card_content"              : posting.content,
                "comment_num"               : PostingComment.objects.filter(posting_id=posting.id).count() if posting.comment.exists() else 0,
                "comment_user_image"        : posting.comment.first().user.image_url if posting.comment.exists() else "None",
                "comment_user_name"         : posting.comment.first().user.name if posting.comment.exists() else "None",
                "comment_content"           : posting.comment.first().content if posting.comment.exists() else "None",
                "posting_like"              : PostingLike.objects.filter(posting_id=posting.id).count(),
                "created_at"                : posting.created_at
                } for posting in postings
        ]
        if sort == 'most_popular':
            posting_list = sorted(posting_list, key=lambda posting: (posting["comment_num"]), reverse=True)
        if sort == 'most_like':
            posting_list = sorted(posting_list, key=lambda posting: (posting["posting_like"]), reverse=True)
        if sort == 'recent':
            posting_list = sorted(posting_list, key=lambda posting: (posting["created_at"]), reverse=True)
        if sort == 'old':
            posting_list = sorted(posting_list, key=lambda posting: (posting["created_at"]))

        sizes  = PostingSize.objects.values()
        styles  = PostingSize.objects.values()
        housings = PostingHousing.objects.values()
        spaces = PostingSpace.objects.values()
        sortings = [{"id" : 1, "name" : "역대인기순"}, {"id" : 2, "name" : "최신순"}, {"id" : 3, "name" : "댓글많은순"}]
        filter_condition = {
                "categories" : [
                    {
                        "id" : 1,
                        "categoryName" : "정렬",
                        "category" : [name for name in list(sortings)]
                        },
                    {
                        "id" : 2,
                        "categoryName" : "주거형태",
                        "category" : [name for name in list(housings)]
                    },
                    {
                        "id" : 3,
                        "categoryName" : "공간",
                        "category" : [name for name in list(spaces)]
                    },
                    {
                        "id" : 4,
                        "categoryName" : "평수",
                        "category" : [name for name in list(sizes)]
                    },
                    {
                        "id" : 5,
                        "categoryName" : "스타일",
                        "category" : [name for name in list(styles)]
                    }]
                }
        return JsonResponse({'message' : posting_list, "message2" : filter_condition}, status=200)
