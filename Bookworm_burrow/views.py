from django.shortcuts import render
from django.views.generic import TemplateView
from posts.models import Post
# Create your views here.


# class Home(TemplateView):
#     template_name = 'index.html'

#     def get_context_data(self, **kwargs):
#         data = Post.objects.all()
#         context = super().get_context_data(**kwargs)
#         context['data'] = data  
#         return context


def home(request):
    data = Post.objects.all()
    # print(data)
    return render(request, 'index.html', {'data': data})
    