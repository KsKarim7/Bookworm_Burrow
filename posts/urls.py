from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    # path('add/', views.add_post, name='add_post'),
    # path('edit/<int:id>', views.edit_post, name='edit_post'),
    path('details/<int:id>/', views.DetailBookView.as_view(), name='detail_post'),
    
    path("borrow/<int:id>", views.Borrowed_Book, name="borrow_book"), 
   
    # path('return/<int:id>', views.Return_book, name='returnbook'),
    
    # path('comments/<int:pk>/', views.Comment_views.as_view(), name='comment_views'),
]