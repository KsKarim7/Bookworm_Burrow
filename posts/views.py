from django.shortcuts import render, redirect, get_object_or_404
from . import forms
from . import models
from django.views.generic import DetailView
from .models import Post
from django.contrib import messages
from django.urls import reverse
from django.urls import reverse_lazy
from .models import BorrowedBookModel
# from library.models import BookModel

# Create your views here.

# def add_post(request):
#     if request.method == 'POST':
#         post_form = forms.PostForm(request.POST) 
#         if post_form.is_valid(): 
#             post_form.save() 
#             return redirect('add_post') 
    
#     else: 
#         post_form = forms.PostForm()
#     return render(request, 'add_post.html', {'form' : post_form})


# def edit_post(request, id):
#     post = models.Post.objects.get(pk=id) 
#     post_form = forms.PostForm(instance=post)
   
#     if request.method == 'POST':
#         post_form = forms.PostForm(request.POST, instance=post) 
#         if post_form.is_valid():
#             post_form.save() 
#             return redirect('homepage') 


class DetailBookView(DetailView):
    model = models.Post
    pk_url_kwarg = 'id'
    template_name = 'book_details.html'
    
    # def post(self, request, *args, **kwargs):
    #     comment_form = forms.CommentForm(data=self.request.POST)
    #     car = self.get_object()
    #     if comment_form.is_valid():
    #         new_comment = comment_form.save(commit=False)
    #         new_comment.car = car
    #         new_comment.save()
    #     return self.get(request, *args, **kwargs)
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     car = self.object #storing car model object
    #     comments = car.comments.all()
    #     comment_form = forms.CommentForm()
        
    #     context['comments'] = comments
    #     context['comment_form'] = comment_form
    #     return context


def Borrowed_Book(request, id):
    book = get_object_or_404(Post, pk=id)

    user_balance = int(request.user.account.balance)
    borrowing_price = int(book.borrowing_price)

    if user_balance >= borrowing_price:
        # # Create and save BorrowedBook instance
        BorrowedBookModel.objects.create(user=request.user, book=book)
        
    
        request.user.account.balance -= borrowing_price
        request.user.account.save()

        messages.success(
            request,
            f'{"{:,.2f}".format(float(borrowing_price))}$ was Borrowed Book successfully'
            )

        # send_transaction_email(request.user, borrowing_price, "Borrowed Book Message", "boored_book_email.html")
    else:
        messages.success(
            request,
            f'{"{:,.2f}".format(float(borrowing_price))}$ Borrowing price is big for your account balance'
            )



    return redirect(reverse("book_details", args=[book.id]))