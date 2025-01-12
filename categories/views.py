# from django.shortcuts import render, redirect
# from . import forms
# # Create your views here.


# INSERT INTO category (name, slug)
# VALUES ('Category Name', 'category-name');

# def add_category(request):
#     if request.method == 'POST':
#         category_form = forms.CategoryForm(request.POST) 
#         if category_form.is_valid():
#             category_form.save() 
#             return redirect('add_category') 
    
#     else: 
#         category_form = forms.CategoryForm()
#     return render(request, 'add_category.html', {'form' : category_form})