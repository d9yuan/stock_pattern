"""stock_pattern URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from pages.views import home_view
from stocks.views import stock_create_view, stock_find_view, stock_detail_view

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls, name='admin'),
    path('create/', stock_create_view, name='create'),
    path('find/', stock_find_view, name='find'),
    path('find/<int:id>/', stock_detail_view, name='detail'), 
]
