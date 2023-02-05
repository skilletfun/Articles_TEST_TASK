from rest_framework import serializers
from .models import Article, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

class ArticleSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(read_only=True, many=True)
    creator = serializers.ReadOnlyField(source='creator.username')

    class Meta:
        model = Article
        fields = ['name', 'creator', 'categories', 'content', 'link', 'create_date', 'edit_date']
