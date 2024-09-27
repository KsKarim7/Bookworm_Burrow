from django.shortcuts import render, redirect, get_object_or_404
from . import forms
from . import models
from django.views.generic import DetailView
from .models import Post
from django.contrib import messages
from django.urls import reverse
from django.urls import reverse_lazy
from .models import BorrowedBookModel
from .forms import ReviewForm
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from datetime import datetime
# from library.models import BookModel

def send_transaction_email(user, amount, subject, template):
        message = render_to_string(template, {
            'user' : user,
            'amount' : amount,
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()


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

    # def get(self, request, id):
    #     book = get_object_or_404(Post, pk=id)
    #     review_form = ReviewForm()
    #     borrowed_book = BorrowedBookModel.objects.filter(user=request.user, book=book).exists()

    #     if borrowed_book:
    #         return render(request, self.template_name, {'form': review_form, 'book': book})
    #     else:
    #         messages.error(request, 'You can only review a book if you have borrowed it.')
    #         return redirect('detail_post', id) 


    def post(self, request, *args, **kwargs):
        review_form = ReviewForm(data=self.request.POST)
        book = self.get_object()
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.book = book
            new_review.user = request.user
            new_review.save()
            
            
        return self.get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        reviews = book.reviews.all()
        review_form = ReviewForm()
        context['reviews'] = reviews
        context['review_form'] = review_form
        context['book'] = book
        return context
    


def Borrow_Book(request, id):
    book = get_object_or_404(Post, pk=id)

    user_balance = int(request.user.account.balance)
    borrowing_price = int(book.price)

    if user_balance >= borrowing_price:
        BorrowedBookModel.objects.create(user=request.user, book=book)
        request.user.account.balance -= borrowing_price
        request.user.account.save()

        messages.success(
            request,
            f'{book.title} has been borrowed for ${"{:,.2f}".format(float(borrowing_price))} successfully! '
            )
    else:
        messages.error(
            request,
            f'${"{:,.2f}".format(float(borrowing_price))} Borrowing price for your desired book has exceeded your balance'
            )
  



    return redirect(reverse("detail_post", args=[book.id]))


def Return_book(request, id):
    record = BorrowedBookModel.objects.get(pk=id)

    
    request.user.account.balance += int(record.book.price)
    request.user.account.save()
    record.delete()
    messages.success(
        request,
        f'Book has been returned successfully!'
        )
    return redirect('profile')

