from django.db import models
from categories.models import Category
from django.core.validators import MaxValueValidator, MinValueValidator

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
    



    
    