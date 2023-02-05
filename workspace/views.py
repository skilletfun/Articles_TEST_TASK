import json
from datetime import datetime

from django.shortcuts import render, redirect
from rest_framework.views import APIView, Response, View
from .models import Category, Article
from .serializers import ArticleSerializer


class WorkspaceView(View):
    def get(self, request):
        return render(request, 'workspace.html')

class CategoriesView(View):
    def get(self, request):
        return render(request, 'categories.html')

class ArticlesView(View):
    def get(self, request):
        return render(request, 'articles.html')

class CategoriesAPIView(APIView):
    ADD_KEY = 'add'
    GET_KEY = 'get'
    DELETE_KEY = 'del'
    RENAME_KEY = 'rename'

    def get(self, request):
        return Response({'categories': [el.name for el in Category.objects.all()]})

    def post(self, request):
        if request.user.is_authenticated:
            if request.data['type'] == self.GET_KEY:
                return Response({'categories': [el.name for el in Category.objects.filter(creator=request.user)]})
            try:
                {
                    self.ADD_KEY: lambda el: Category.objects.create(name=el.data['name'], creator=el.user),
                    self.DELETE_KEY: lambda el: Category.objects.filter(name=el.data['name'], creator=el.user).delete(),
                    self.RENAME_KEY: lambda el: Category.objects.filter(name=el.data['name'], creator=el.user).update(name=el.data['newname'])
                }[request.data['type']](request)
            except:
                pass
        return CategoriesView().get(request)


class ArticlesAPIView(APIView):
    ADD_KEY = 'add'
    DELETE_KEY = 'del'
    EDIT_KEY = 'edit'
    GET_KEY = 'get'
    GET_ALL_KEY = '__all__'

    def get(self, request):
        if request.user.is_authenticated:
            return Response({'articles': [el.id for el in Article.objects.filter(creator=request.user)]})

    def post(self, request):
        if request.data['type'] == self.GET_KEY:
            return self.get_objects(request)
        if request.user.is_authenticated:
            solve_dict = {
                self.ADD_KEY: lambda el: self.create_obj(el),
                self.DELETE_KEY: lambda el: self.delete_obj(el),
                self.EDIT_KEY: lambda el: self.update_obj(el)
            }
            if request.data['type'] in solve_dict:
                return solve_dict[request.data['type']](request)
        return Response({'error': 'Undefined requested type'})


    def create_obj(self, request):
        obj = Article.objects.create(
            name=request.data['name'],
            creator=request.user,
            content=request.data['content'],
            link=request.data['link']
        )
        for cat in request.data['categories'].lower().split():
            cat_obj = Category.objects.filter(name=cat)
            if cat_obj.exists():
                obj.categories.add(cat_obj[0])
        return ArticlesView().get(request)

    def update_obj(self, request):
        obj = Article.objects.get(id=request.data['pk'])
        obj.categories.remove(obj)
        obj.update(
            name=request.data['name'],
            content=request.data['content'],
            link=request.data['link'],
            edit_date=datetime.now()
        )
        for cat in request.data['categories'].lower().split():
            obj.categories.add(Category.objects.get(name=cat))
        return ArticlesView().get(request)

    def delete_obj(self, request):
        Article.objects.filter(id=request.data['pk']).delete()
        return ArticlesView().get(request)

    def get_objects(self, request):
        if request.data['category'] == self.GET_ALL_KEY:
            queryset = Article.objects.all()
        else:
            queryset = Article.objects.filter(categories=Category.objects.get(name=request.data['category']))
        return Response({'articles': ArticleSerializer(queryset, many=True).data})
