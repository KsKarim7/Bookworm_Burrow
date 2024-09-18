from django.contrib import admin
from django.urls import path,include
from core.views import Home

urlpatterns = [
    path('',Home.as_view()),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
]