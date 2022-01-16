from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from states.models import State, Author, Category, Tag
from states.serializers import AuthorSerializer, CategorySerializer, TagSerializer, StateSerializer
from django.core.exceptions import FieldError


class AuthorList(APIView):

    def get_object(self, **kwargs):
        try:
            return Author.objects.get(**kwargs)
        except Author.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        author = request.query_params.dict()
        if author:
            author_obj = [self.get_object(**author)]
        else:
            author_obj = Author.objects.all()
        serializer = AuthorSerializer(author_obj, many=True)
        return Response(serializer.data)

    def post(self, request: Request, format=None):
        serializer = AuthorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        if not request.query_params:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        author = self.get_object(**request.query_params.dict())
        serializer = AuthorSerializer(author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        if not request.query_params:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        author = self.get_object(**request.query_params.dict())
        author_data = Author
        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AuthorDetail(APIView):

    def get_object(self, pk):
        try:
            return Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        author = self.get_object(pk)
        serializer = AuthorSerializer(author)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        author = self.get_object(pk)
        serializer = AuthorSerializer(author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        author = self.get_object(pk)
        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryList(APIView):

    def get_object(self, **kwargs):
        try:
            return Category.objects.get(**kwargs)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        category = request.query_params.dict()
        if category:
            category_obj = [self.get_object(**category)]
        else:
            category_obj = Category.objects.all()
        serializer = CategorySerializer(category_obj, many=True)
        return Response(serializer.data)

    def post(self, request: Request, format=None):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        if not request.query_params:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        category = self.get_object(**request.query_params.dict())
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        if not request.query_params:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        category = self.get_object(**request.query_params.dict())
        category_data = Category
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryDetail(APIView):
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagList(APIView):

    def get_object(self, **kwargs):
        try:
            return Tag.objects.get(**kwargs)
        except Tag.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        tag = request.query_params.dict()
        if tag:
            tag_obj = [self.get_object(**tag)]
        else:
            tag_obj = Tag.objects.all()
        serializer = TagSerializer(tag_obj, many=True)
        return Response(serializer.data)

    def post(self, request: Request, format=None):
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        if not request.query_params:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        tag = self.get_object(**request.query_params.dict())
        serializer = TagSerializer(tag, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        if not request.query_params:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        tag = self.get_object(**request.query_params.dict())
        tag_data = tag
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagDetail(APIView):
    def get_object(self, pk):
        try:
            return Tag.objects.get(pk=pk)
        except Tag.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        tag = self.get_object(pk)
        serializer = TagSerializer(tag)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        tag = self.get_object(pk)
        serializer = TagSerializer(tag, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StateList(APIView):
    def get_QuerySet(self, **kwargs):
        condition = kwargs
        if 'date' in condition:
            condition = {'date__contains': condition['date']}
        try:
            for obj in State.objects.filter(**condition):
                yield obj
        except FieldError:
            raise Http404

    def get_read_serializer(self, **kwargs):
        data = []
        condition = kwargs
        for i in self.get_QuerySet(**condition):
            copy_ser = dict(StateSerializer(i).data)
            author_id = StateSerializer(i).data['author']
            category_id = StateSerializer(i).data['category']
            tag_id = StateSerializer(i).data['tag']
            author_fields = AuthorSerializer(Author.objects.get(id=author_id)).data
            category_fields = CategorySerializer(Category.objects.get(id=category_id)).data
            tag_fields = [TagSerializer(Tag.objects.get(id=j)).data for j in tag_id]
            copy_ser['author'] = author_fields
            copy_ser['category'] = category_fields
            copy_ser['tag'] = tag_fields
            data.append(copy_ser)
        return data

    def get(self, request, format=None):
        # if not request.query_params:
        #     return Response(status.HTTP_400_BAD_REQUEST)
        contents = self.get_read_serializer(**request.query_params.dict())
        if contents:
            return Response(contents)
        else:
            return Response({'error': '404 not found'}, status.HTTP_404_NOT_FOUND)

    def post(self, request: Request, format=None):
        serializer = StateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
        valid = False
        for i in self.get_QuerySet(**request.query_params.dict()):
            serializer = StateSerializer(i, data=request.data)
            if serializer.is_valid():
                valid = True
                serializer.save()
        contents = self.get_read_serializer(**request.query_params.dict())
        if valid:#contents:
            # return Response(contents)
            return Response(contents)
        else:
            return Response({'error': 'Bad request'}, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        valid = False
        if not request.query_params:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        for i in self.get_QuerySet(**request.query_params.dict()):
            i.delete()
            valid = True
        if valid:
            return Response(request.query_params, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class StateDetail(APIView):

    def get_QuerySet(self, **kwargs):
        condition = kwargs
        if 'date' in condition:
            condition = {'date__contains': condition['date']}
        try:
            for obj in State.objects.filter(**condition):
                yield obj
        except FieldError:
            raise Http404

    def get_read_serializer(self, nm, pk):
        data = []
        condition = {nm: pk}
        for i in self.get_QuerySet(**condition):
            serializer = StateSerializer(i)
            copy_ser = dict(serializer.data)
            author_id = StateSerializer(i).data['author']
            category_id = StateSerializer(i).data['category']
            tag_id = StateSerializer(i).data['tag']
            author_fields = AuthorSerializer(Author.objects.get(id=author_id)).data
            category_fields = CategorySerializer(Category.objects.get(id=category_id)).data
            tag_fields = [TagSerializer(Tag.objects.get(id=j)).data for j in tag_id]
            copy_ser['author'] = author_fields
            copy_ser['category'] = category_fields
            copy_ser['tag'] = tag_fields
            data.append(copy_ser)
        # else:
        #     serializer = StateSerializer(State.objects.get(**condition))
        return data

    def get(self, request, nm, pk, format=None):
        contents = self.get_read_serializer(nm, pk)
        if contents:
            return Response(contents)
        else:
            return Response({'error': 'Bad request'}, status.HTTP_404_NOT_FOUND)

    def put(self, request, nm, pk, format=None):
        condition = {nm: pk}
        valid = False
        for i in self.get_QuerySet(**condition):
            serializer = StateSerializer(i, data=request.data)
            if serializer.is_valid():
                valid = True
                serializer.save()
        contents = self.get_read_serializer(nm, pk)
        if valid:#contents:
            return Response(contents)
        else:
            return Response({'error': 'Bad request'}, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, nm, pk, format=None):
        condition = {nm: pk}
        valid = False
        for i in self.get_QuerySet(**condition):
            i.delete()
            valid = True
        if valid:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)
