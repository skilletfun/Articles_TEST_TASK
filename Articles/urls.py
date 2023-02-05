"""Articles URL Configuration

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
from django.urls import path, include
from workspace.views import WorkspaceView, ArticlesView, CategoriesView, CategoriesAPIView, ArticlesAPIView

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    path('', WorkspaceView.as_view(), name='home'),
    path('articles/', ArticlesView.as_view(), name='articles'),
    path('categories/', CategoriesView.as_view(), name='categories'),
    path('api/v1/categories/', CategoriesAPIView.as_view(), name='api_categories'),
    path('api/v1/articles/', ArticlesAPIView.as_view(), name='api_articles'),
]
