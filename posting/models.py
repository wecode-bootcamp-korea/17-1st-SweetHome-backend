from django.db import models

from user.models import User

class Posting(models.Model):
    user       = models.ForeignKey('user.User', on_delete=models.CASCADE)
    image_url  = models.URLField(max_length=2000)
    content    = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    size       = models.ForeignKey('PostingSize', on_delete=models.CASCADE)
    housing    = models.ForeignKey('PostingHousing', on_delete=models.CASCADE)
    style      = models.ForeignKey('PostingStyle', on_delete=models.CASCADE)
    space      = models.ForeignKey('PostingSpace', on_delete=models.CASCADE)
    like_user  = models.ManyToManyField('user.User', through='PostingLike', related_name='user_like_posting')
    scrap_user = models.ManyToManyField('user.User', through='PostingScrap', related_name='user_scrap_posting')

    class Meta:
        db_table = 'postings'

class PostingSize(models.Model):
    name = models.CharField(max_length=45, unique=True)

    class Meta:
        db_table = 'posting_sizes'

class PostingHousing(models.Model):
    name = models.CharField(max_length=45, unique=True)

    class Meta:
        db_table = 'posting_housings'

class PostingStyle(models.Model):
    name = models.CharField(max_length=45, unique=True)

    class Meta:
        db_table = 'posting_styles'

class PostingSpace(models.Model):
    name = models.CharField(max_length=45, unique=True)

    class Meta:
        db_table = 'posting_spaces'

class PostingLike(models.Model):
    user    = models.ForeignKey('user.User', on_delete=models.CASCADE)
    posting = models.ForeignKey('Posting', on_delete=models.CASCADE)

    class Meta:
        db_table = 'posting_likes'

class PostingScrap(models.Model):
    user    = models.ForeignKey('user.User', on_delete=models.CASCADE)
    posting = models.ForeignKey('Posting', on_delete=models.CASCADE)

    class Meta:
        db_table = 'posting_scraps'

class PostingComment(models.Model):
    user       = models.ForeignKey('user.User', on_delete=models.CASCADE)
    posting    = models.ForeignKey('Posting', on_delete=models.CASCADE, related_name='comment')
    content    = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'posting_comments'
