from django.contrib import admin
from django.urls import path,include
from core.views import Home
from . import views

urlpatterns = [
    # path('', Home.as_view(),name = 'home'),
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    # path('categories/', include('categories.urls')),
]
