from django.db import models
from categories.models import Category
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
# from .models import Post


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    category = models.ManyToManyField(Category) 
    price = models.IntegerField()
    rating = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    image = models.ImageField(upload_to='posts/media/uploads/',blank = True, null = True)
    
    def __str__(self):
        return self.title 
    
class BorrowedBookModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Post, on_delete=models.CASCADE)
    borrowed_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"



    
    