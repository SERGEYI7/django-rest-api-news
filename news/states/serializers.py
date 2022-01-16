from rest_framework import serializers
from states.models import State, Author, Category, Tag


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'title']


class StateSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    # author = AuthorSerializer(Base.Author.objects.all())
    # category = CategorySerializer(Base.Category.objects.all())
    # tag = TagSerializer(Base.Tag.objects.all())

    class Meta:
        model = State
        fields = ['id', 'title', 'summary', 'content', 'author', 'category', 'tag', 'date']
