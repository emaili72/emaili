from django.db import models
from account.models import User

class Category(models.Model):
    slug = models.SlugField(max_length=255,primary_key=True)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
class Post(models.Model):
    author = models.ForeignKey(User,related_name='posts',on_delete=models.CASCADE)
    title = models.CharField(max_length=100,blank=False)
    body = models.TextField()
    image = models.ImageField(upload_to='post',blank=True,null=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='post')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title