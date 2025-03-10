from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('add/',views.AddPostCreateView.as_view(),name='add_post'),
    path('edit/<int:id>/', views.EditPostView.as_view(), name='edit_post'),
    path('delete/<int:id>/', views.DeletePostView.as_view(), name='delete_post'),
    path('details/<int:id>/', views.DetailBookView.as_view(), name='detail_post'),
    path('borrow/<int:id>/', views.Borrow_Book, name="borrow_book"), 
    path('return/<int:id>', views.Return_book, name='return_book'),
    
]