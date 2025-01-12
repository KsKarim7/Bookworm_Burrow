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
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView,UpdateView,DeleteView,DetailView
from django.contrib.auth.decorators import user_passes_test

def is_admin(user):
    return user.is_superuser  # Checks if the user is an admin

def send_transaction_email(user, amount, subject, template):
        message = render_to_string(template, {
            'user' : user,
            'amount' : amount,
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()



# INSERT INTO post (title, description, price, rating, image)
# VALUES ('Sample Title', 'This is a sample description.', 500, 4, 'posts/media/uploads/sample.jpg');

# @method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_admin), name='dispatch')
class AddPostCreateView(CreateView):
    model = models.Post
    form_class = forms.PostForm
    template_name = 'add_post.html'
    success_url = reverse_lazy('add_post')
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    

# UPDATE post
# SET 
#     title = 'Updated Title',
#     description = 'Updated description.',
#     price = 600,
#     rating = 4,
#     image = 'posts/media/uploads/updated_image.jpg'
# WHERE id = 1;
# @method_decorator(login_required, name = 'dispatch')
@method_decorator(user_passes_test(is_admin), name='dispatch')
class EditPostView(UpdateView):
    model = models.Post
    form_class = forms.PostForm
    template_name = 'add_post.html'
    # pk_url_kwargs = 'id'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return self.model.objects.get(id=self.kwargs['id'])


# DELETE FROM post
# WHERE id = 1; 
# @method_decorator(login_required, name='dispatch')
@method_decorator(user_passes_test(is_admin), name='dispatch')
class DeletePostView(DeleteView):
    model = models.Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')
    pk_url_kwarg = 'id'


# SELECT *
# FROM post
# WHERE id = <id>;
# SELECT *
# FROM post
# WHERE id = <id>;
# SELECT *
# FROM review
# WHERE book_id = <id>;
# INSERT INTO review (book_id, user_id, body, created_on)
# VALUES (<post_id>, <user_id>, '<review_body>', NOW());


class DetailBookView(DetailView):
    model = models.Post
    pk_url_kwarg = 'id'
    template_name = 'book_details.html'

    def post(self, request, *args, **kwargs):
        review_form = ReviewForm(data=self.request.POST)
        book = self.get_object()

        if not request.user.is_authenticated:
            messages.error(request, "You need to log in to submit a review.")
            return redirect("login")  
        
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
    


# SELECT *
# FROM post
# WHERE id = <id>;
# SELECT balance
# FROM userlibraryaccount
# WHERE user_id = <user_id>;
# INSERT INTO borrowedbookmodel (user_id, book_id, borrowed_date)
# VALUES (<user_id>, <book_id>, NOW());
# UPDATE userlibraryaccount
# SET balance = balance - <borrowing_price>
# WHERE user_id = <user_id>;


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



# SELECT *
# FROM borrowedbookmodel
# WHERE id = <id>;
# UPDATE userlibraryaccount
# SET balance = balance + <book_price>
# WHERE user_id = <user_id>;
# DELETE FROM borrowedbookmodel
# WHERE id = <id>;

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

