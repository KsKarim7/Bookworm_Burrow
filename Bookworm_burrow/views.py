from django.shortcuts import render
from django.views.generic import TemplateView
from posts.models import Post
from categories.models import Category
# Create your views here.


# class Home(TemplateView):
#     template_name = 'index.html'

#     def get_context_data(self, **kwargs):
#         data = Post.objects.all()
#         context = super().get_context_data(**kwargs)
#         context['data'] = data  
#         return context


def home(request,category_slug = None):
    data = Post.objects.all() 
    if category_slug is not None: 
        category = Category.objects.get(slug = category_slug) 
        data = Post.objects.filter(category  = category) 
    categories = Category.objects.all() 
    return render(request, 'index.html', {'data' : data, 'category' : categories})

    data = Post.objects.all()
    if category_slug is not None:
        category = Category.objects.get(slug = category_slug)
        data = Post.objects.filter(category  = category)
    categories = Category.objects.all()
    return render(request, 'home.html', {'data' : data, 'category' : categories})

    cars = Car.objects.all()
    if(brand_slug is not None):
        brand = Brand.objects.get(slug = brand_slug)
        cars = Car.objects.filter(brand = brand)
    brands = Brand.objects.all()
    return render(req, 'home.html', {'car' : cars, 'brand' : brands})
    