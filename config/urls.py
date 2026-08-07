"""
URL configuration for host Django project wrapper.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home_view(request):
    return HttpResponse("<h1>Bahari Inventory System</h1><p><a href='/admin/'>Go to Admin Dashboard</a></p>")

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('inventory.api.urls')),
]
