"""
URL configuration for myworkshop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import include, path
from workshop import views, urls

urlpatterns = [
    # path('', include('django.contrib.auth.urls')),
    path('',views.MyLoginView.as_view(),name="login"),
    path('sign-up', views.sign_up, name="sign-up" ),
    path('admin/', admin.site.urls),
    path('workshop/', include("workshop.urls"))
]
