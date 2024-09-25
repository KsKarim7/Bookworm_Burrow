from . import models
from django.contrib import admin

# Register your models here.

admin.site.register(models.Post)
admin.site.register(models.BorrowedBookModel)
# admin.site.register(models.Comment)