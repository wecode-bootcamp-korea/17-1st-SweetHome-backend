from django.db      import models

class User(models.Model):
    email       = models.CharField(max_length=45, unique=True)
    password    = models.CharField(max_length=300)
    name        = models.CharField(max_length=45, unique=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    image_url   = models.URLField(max_length=2000, default="https://www.flaticon.com/svg/vstatic/svg/742/742751.svg?token=exp=1613546907~hmac=a021c08f8195374a8901fc3eccbb71b7")
    description = models.CharField(max_length=45, null=True)
    
    class Meta:
        db_table = 'users'

class Follow(models.Model):
    from_user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='following')
    to_user   = models.ForeignKey('User', on_delete=models.CASCADE, related_name='follower')

    class Meta:
        db_table = 'follows'