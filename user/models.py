from django.db      import models

class User(models.Model):
    email       = models.CharField(max_length=45, unique=True)
    password    = models.CharField(max_length=300)
    name        = models.CharField(max_length=45, unique=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    image_url   = models.URLField(max_length=2000, default="https://media.vlpt.us/images/c_hyun403/post/7b35d3bb-44be-41bf-8192-0ccc426b465c/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202021-02-26%20%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE%2012.53.02.png")
    description = models.CharField(max_length=45, null=True)
    
    class Meta:
        db_table = 'users'

class Follow(models.Model):
    from_user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='following')
    to_user   = models.ForeignKey('User', on_delete=models.CASCADE, related_name='follower')

    class Meta:
        db_table = 'follows'
