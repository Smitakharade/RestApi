"""rest_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from rest_app import views  # import views form your app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/get_emp/<int:pk>/', views.get_emp), # in postman we need to pass an id in url for that we need to use this url 
    path('api/get_emp/', views.get_emp),
    path('api/create_emp/', views.create_emp),
    path('api/update_emp/', views.update_emp),
    path('api/Pupdate_emp/', views.partialupdate_emp),
    path('api/delete_emp/', views.delete_emp),

    #----------------------------------------------------------
    #  url for all crud operations 
    path('api/all_crud_operations/<int:pk>/', views.all_crud_operations),   # in postman we need to pass an id in url for that we need to use this url 
    path('api/all_crud_operations/', views.all_crud_operations),
]
