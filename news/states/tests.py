import json
from django.test import TestCase, Client, SimpleTestCase
from django.urls import reverse
from rest_framework.serializers import ListSerializer
from states.models import State, Tag, Author, Category
from states.serializers import StateSerializer, TagSerializer, AuthorSerializer, CategorySerializer
from rest_framework import status


class GetAllStatesTest(TestCase):

    client = Client()

    def setUp(self):

        data_author1 = {'first_name': 'Dima', 'last_name': 'Voronin'}
        data_author2 = {'first_name': 'Vova', 'last_name': 'Vinnica'}
        data_author3 = {'first_name': 'Bob', 'last_name': 'Gladkih'}
        data_author4 = {'first_name': 'Igor', 'last_name': 'Similyar'}
        data_author5 = {'first_name': 'Sergeyi', 'last_name': 'Poleshchuk'}
        data_authors = [data_author1, data_author2, data_author3, data_author4, data_author5]
        for author in data_authors:
            self.author = Author.objects.create(**author)

        data_category1 = {'title': 'Politics'}
        data_category2 = {'title': 'Games'}
        data_category3 = {'title': 'Books'}
        data_category4 = {'title': 'Science'}
        data_category5 = {'title': 'Economics'}
        data_categories = [data_category1, data_category2, data_category3, data_category4, data_category5]
        for category in data_categories:
            self.category = Category.objects.create(**category)

        data_tag1 = {'title': 'Peoples'}
        data_tag2 = {'title': 'Shopp'}
        data_tag3 = {'title': 'Celebrity'}
        data_tag4 = {'title': 'Technology'}
        data_tag5 = {'title': 'Crypto coin'}
        data_tags = [data_tag1, data_tag2, data_tag3, data_tag4, data_tag5]
        for tag in data_tags:
            self.tag = Tag.objects.create(**tag)

        data_state1 = [{'title': 'games', 'summary': 'games cool',
                        'content': 'games very cool', 'author': Author.objects.get(id=1),
                        'category': Category.objects.get(id=1), 'date': '2022-01-14'}, [1, 2]]
        data_state2 = [{'title': 'Evolution', 'summary': 'Evolution humans',
                        'content': 'Man evolved from ape', 'author': Author.objects.get(id=2),
                        'category': Category.objects.get(id=2), 'date': '2022-01-14'}, [1, 3]]
        data_state3 = [{'title': 'Bitcoin', 'summary': 'Bitcoin has risen in price',
                        'content': 'Bitcoin has risen in price again', 'author': Author.objects.get(id=3),
                        'category': Category.objects.get(id=3), 'date': '2022-01-15'}, [2, 3]]
        data_state4 = [{'title': 'New technology', 'summary': 'New technology created',
                        'content': 'A new technology has been created to make life easier',
                        'author': Author.objects.get(id=4), 'category': Category.objects.get(id=4),
                        'date': '2022-01-16'}, [4, 3]]
        data_state5 = [{'title': 'New president', 'summary': 'New president was elected',
                        'content': 'The people elected a new president', 'author': Author.objects.get(id=5),
                        'category': Category.objects.get(id=1), 'date': '2022-01-15'}, [3, 5]]
        data_states = [data_state1, data_state2, data_state3, data_state4, data_state5]
        for full_state, tags in data_states:
            self.state = State.objects.create(**full_state)
            self.state.tag.add(Tag.objects.get(id=tags[0]), Tag.objects.get(id=tags[1]))

    def test_get_all_authors(self):
        response = self.client.get(reverse('get_authors_with_params'))
        authors = Author.objects.all()
        authors_serializer = AuthorSerializer(authors, many=True)
        self.assertEqual(response.data, authors_serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_author_with_params_valid(self):
        author_id = self.author.id - 1
        response = self.client.get(reverse('get_authors_with_params')+f'?id={author_id}')
        author = Author.objects.get(id=author_id)
        serializer = AuthorSerializer(author)
        self.assertEqual(response.data[0], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_author_with_params_invalid(self):
        author_id = self.author.id + 1
        response = self.client.get(reverse('get_authors_with_params')+f'?id={author_id}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_author_with_pk_valid(self):
        author_pk = self.author.pk
        response = self.client.get(reverse('get_authors_with_pk', kwargs={'pk': author_pk}))
        author = Author.objects.get(pk=author_pk)
        serializer = AuthorSerializer(author)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_author_with_pk_invalid(self):
        author_pk = self.author.pk + 1
        response = self.client.get(reverse('get_authors_with_pk', kwargs={'pk': author_pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_author_valid(self):
        data = json.dumps({'first_name': 'astroloy', 'last_name': 'Dima'})
        response = self.client.post(reverse('get_authors_with_params'), data=data,
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_author_invalid(self):
        data = json.dumps({'tittle': 'astroloewdrvwsdvfewsdgy'})
        response = self.client.post(reverse('get_authors_with_params'), data=data,
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(reverse('get_authors_with_params'),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_author_with_params_valid(self):
        data = json.dumps({'first_name': 'astrophysics', 'last_name': 'Valera'})
        author_id = self.author.id
        response = self.client.put(reverse('get_authors_with_params')+f'?id={author_id}', data=data,
                                   content_type='application/json')
        author_obj = Author.objects.get(id=author_id)
        serializer = AuthorSerializer(author_obj)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_author_with_params_invalid(self):
        data = json.dumps({'titlee': 'astrology'})
        author_id = self.author.id
        response = self.client.put(reverse('get_authors_with_params') + f'?id={author_id}', data=data,
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        author_id = self.author.id + 1
        response = self.client.put(reverse('get_authors_with_params') + f'?id={author_id}', data=data,
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.put(reverse('get_authors_with_params'), data=data,
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_author_with_pk_valid(self):
        data = json.dumps({'first_name': 'astrophysics', 'last_name': 'Valera'})
        author_pk = self.author.pk
        response = self.client.put(reverse('get_authors_with_pk', kwargs={'pk': author_pk}), data=data,
                                   content_type='application/json')
        author_obj = Author.objects.get(id=author_pk)
        serializer = AuthorSerializer(author_obj)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_author_with_pk_invalid(self):
        data = json.dumps({'titlee': 'astrology'})
        author_pk = self.author.pk
        response = self.client.put(reverse('get_authors_with_pk', kwargs={'pk': author_pk}), data=data,
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_author_with_params_valid(self):
        author_id = self.author.id
        response = self.client.delete(reverse('get_authors_with_params')+f'?id={author_id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_author_with_params_invalid(self):
        author_id = self.author.id + 1
        response = self.client.delete(reverse('get_authors_with_params') + f'?id={author_id}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.delete(reverse('get_authors_with_params'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_delete_author_with_pk_valid(self):
        author_pk = self.author.pk
        response = self.client.delete(reverse('get_authors_with_pk', kwargs={'pk': author_pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_author_with_pk_invalid(self):
        author_pk = self.author.pk + 1
        response = self.client.delete(reverse('get_authors_with_pk', kwargs={'pk': author_pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all_categories(self):
        response = self.client.get(reverse('get_categories_with_params'))
        categories = Category.objects.all()
        categories_serializer = CategorySerializer(categories, many=True)
        self.assertEqual(response.data, categories_serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_category_with_params_valid(self):
        category_id = self.category.id
        response = self.client.get(reverse('get_categories_with_params')+f'?id={category_id}')
        category = Category.objects.get(id=category_id)
        serializer = CategorySerializer(category)
        self.assertEqual(response.data[0], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_category_with_params_invalid(self):
        category_id = self.category.id + 1
        response = self.client.get(reverse('get_categories_with_params')+f'?id={category_id}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_category_with_pk_valid(self):
        category_pk = self.category.pk
        response = self.client.get(reverse('get_categories_with_pk', kwargs={'pk': category_pk}))
        category = Category.objects.get(pk=category_pk)
        serializer = CategorySerializer(category)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_category_with_pk_invalid(self):
        category_pk = self.category.pk + 1
        response = self.client.get(reverse('get_categories_with_pk', kwargs={'pk': category_pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_category_valid(self):
        data = json.dumps({'title': 'astrology'})
        response = self.client.post(reverse('get_categories_with_params'), data=data,
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_category_invalid(self):
        data = json.dumps({'tittle': 'astroloewdrvwsdvfewsdgy'})
        response = self.client.post(reverse('get_categories_with_params'), data=data,
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(reverse('get_categories_with_params'),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_category_with_params_valid(self):
        data = json.dumps({'title': 'astrology'})
        category_id = self.category.id
        response = self.client.put(reverse('get_categories_with_params')+f'?id={category_id}', data=data,
                                   content_type='application/json')
        category_obj = Category.objects.get(id=category_id)
        serializer = CategorySerializer(category_obj)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_category_with_params_invalid(self):
        data = json.dumps({'titlee': 'astrology'})
        category_id = self.category.id
        response = self.client.put(reverse('get_categories_with_params') + f'?id={category_id}', data=data,
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = json.dumps({'title': 'astrology'})
        category_id = self.category.id + 1
        response = self.client.put(reverse('get_categories_with_params') + f'?id={category_id}', data=data,
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        data = json.dumps({'title': 'astrology'})
        response = self.client.put(reverse('get_categories_with_params'), data=data,
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_put_category_with_pk_valid(self):
        data = json.dumps({'title': 'astrology'})
        category_pk = self.category.pk
        response = self.client.put(reverse('get_categories_with_pk', kwargs={'pk': category_pk}), data=data,
                                   content_type='application/json')
        category_obj = Category.objects.get(id=category_pk)
        serializer = CategorySerializer(category_obj)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_category_with_pk_invalid(self):
        data = json.dumps({'titlee': 'astrology'})
        category_pk = self.category.pk
        response = self.client.put(reverse('get_categories_with_pk', kwargs={'pk': category_pk}), data=data,
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_category_with_params_valid(self):
        category_id = self.category.id
        response = self.client.delete(reverse('get_categories_with_params')+f'?id={category_id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_category_with_params_invalid(self):
        category_id = self.category.id + 1
        response = self.client.delete(reverse('get_categories_with_params') + f'?id={category_id}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.delete(reverse('get_categories_with_params'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_category_with_pk_valid(self):
        category_pk = self.category.pk
        response = self.client.delete(reverse('get_categories_with_pk', kwargs={'pk': category_pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_category_with_pk_invalid(self):
        category_pk = self.category.pk + 1
        response = self.client.delete(reverse('get_categories_with_pk', kwargs={'pk': category_pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all_tags(self):
        response = self.client.get(reverse('get_tags_with_params'))
        tags = Tag.objects.all()
        tags_serializer = TagSerializer(tags, many=True)
        self.assertEqual(response.data, tags_serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_tag_with_params_valid(self):
        tag_id = self.tag.id - 1
        response = self.client.get(reverse('get_tags_with_params')+f'?id={tag_id}')
        category = Tag.objects.get(id=tag_id)
        serializer = TagSerializer(category)
        self.assertEqual(response.data[0], serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_tag_with_params_invalid(self):
        tag_id = self.tag.id + 1
        response = self.client.get(reverse('get_tags_with_params')+f'?id={tag_id}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_tag_with_pk_valid(self):
        tag_pk = self.tag.pk
        response = self.client.get(reverse('get_tags_with_pk', kwargs={'pk': tag_pk}))
        category = Tag.objects.get(pk=tag_pk)
        serializer = TagSerializer(category)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_tag_with_pk_invalid(self):
        tag_pk = self.tag.pk + 1
        response = self.client.get(reverse('get_tags_with_pk', kwargs={'pk': tag_pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_tag_valid(self):
        data = json.dumps({'title': 'astrology'})
        response = self.client.post(reverse('get_tags_with_params'), data=data,
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_tag_invalid(self):
        data = json.dumps({'tittle': 'astroloewdrvwsdvfewsdgy'})
        response = self.client.post(reverse('get_tags_with_params'), data=data,
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_tag_with_params_valid(self):
        data = json.dumps({'title': 'astrology'})
        tag_id = self.tag.id
        response = self.client.put(reverse('get_tags_with_params')+f'?id={tag_id}', data=data,
                                   content_type='application/json')
        tag_obj = Tag.objects.get(id=tag_id)
        serializer = TagSerializer(tag_obj)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_tag_with_params_invalid(self):
        data = json.dumps({'titlee': 'astrology'})
        tag_id = self.tag.id
        response = self.client.put(reverse('get_tags_with_params') + f'?id={tag_id}', data=data,
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.put(reverse('get_tags_with_params'), data=data,
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_tag_with_pk_valid(self):
        data = json.dumps({'title': 'astrology'})
        tag_pk = self.tag.pk
        response = self.client.put(reverse('get_tags_with_pk', kwargs={'pk': tag_pk}), data=data,
                                   content_type='application/json')
        tag_obj = Tag.objects.get(id=tag_pk)
        serializer = TagSerializer(tag_obj)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_tag_with_pk_invalid(self):
        data = json.dumps({'titlee': 'astrology'})
        tag_pk = self.tag.pk
        response = self.client.put(reverse('get_tags_with_pk', kwargs={'pk': tag_pk}), data=data,
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_tag_with_params_valid(self):
        tag_id = self.tag.id
        response = self.client.delete(reverse('get_tags_with_params')+f'?id={tag_id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_tag_with_params_invalid(self):
        tag_id = self.tag.id + 1
        response = self.client.delete(reverse('get_tags_with_params') + f'?id={tag_id}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.delete(reverse('get_tags_with_params'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_tag_with_pk_valid(self):
        tag_pk = self.tag.pk
        response = self.client.delete(reverse('get_tags_with_pk', kwargs={'pk': tag_pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_tag_with_pk_invalid(self):
        tag_pk = self.tag.pk + 1
        response = self.client.delete(reverse('get_tags_with_pk', kwargs={'pk': tag_pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def read_state_serializer(self, state_serializer):
        ser = []
        if isinstance(state_serializer, ListSerializer):
            iter_obj = state_serializer.data
        elif isinstance(state_serializer, StateSerializer):
            iter_obj = [state_serializer.data]
        for i in iter_obj:
            i['author'] = AuthorSerializer(Author.objects.get(id=i['author'])).data
            i['category'] = CategorySerializer(Category.objects.get(id=i['category'])).data
            i['tag'] = [TagSerializer(Tag.objects.get(id=i['tag'][0])).data,
                        TagSerializer(Tag.objects.get(id=i['tag'][1])).data]
            ser.append(dict(i))
        return ser

    def test_get_all_states(self):
        response = self.client.get(reverse('get_states_with_params'))
        states = State.objects.all()
        states_serializer = StateSerializer(states, many=True)
        self.assertEqual(response.data, self.read_state_serializer(states_serializer))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_state_with_params_valid(self):
        state_id = self.state.id - 1
        response = self.client.get(reverse('get_states_with_params')+f'?id={state_id}')
        state = State.objects.get(id=state_id)
        state_serializer = StateSerializer(state)
        self.assertEqual(response.data, self.read_state_serializer(state_serializer))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_state_with_params_invalid(self):
        state_id = self.state.id + 1
        response = self.client.get(reverse('get_states_with_params')+f'?id={state_id}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_get_state_with_pk_valid(self):
        state_pk = self.state.pk
        response = self.client.get(reverse('get_states_with_pk', kwargs={'nm': 'id', 'pk': state_pk}))
        state = State.objects.get(pk=state_pk)
        state_serializer = StateSerializer(state)
        self.assertEqual(response.data, self.read_state_serializer(state_serializer))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_state_with_pk_invalid(self):
        state_pk = self.state.pk + 1
        response = self.client.get(reverse('get_states_with_pk', kwargs={'nm': 'id', 'pk': state_pk}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_state_valid(self):
        data = json.dumps({'title': 'games', 'summary': 'games cool',
                                  'content': 'games very cool', 'author': 1,
                                  'category': 1, 'tag': [1, 2]})
        response = self.client.post(reverse('get_states_with_params'), data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_state_invalid(self):
        data = json.dumps({'tiiiittle': 'games', 'summary': 'games cool',
                                  'content': 'games very cool', 'auyttyytthor': 1,
                                  'category': 1, 'tag': [1, 2]})
        response = self.client.post(reverse('get_states_with_params'), data=data, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_state_with_params_valid(self):
        data = json.dumps({'title': 'games EDITABLE', 'summary': 'games cool',
                                  'content': 'games very cool', 'author': 1,
                                  'category': 1, 'tag': [1, 2]})
        state_id = self.state.id - 1
        response = self.client.put(reverse('get_states_with_params')+f'?id={state_id}', data=data,
                                   content_type='application/json')
        state_obj = State.objects.get(id=state_id)
        serializer = StateSerializer(state_obj)
        self.assertEqual(response.data, self.read_state_serializer(serializer))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_state_with_params_invalid(self):
        data = json.dumps({'titlee': 'astrology'})
        state_id = self.state.id
        response = self.client.put(reverse('get_states_with_params') + f'?id={state_id}', data=data,
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_state_with_pk_valid(self):
        data = json.dumps({'title': 'games EDITABLE', 'summary': 'games cool',
                           'content': 'games very cool', 'author': 1,
                           'category': 1, 'tag': [1, 2]})
        state_pk = self.state.pk
        response = self.client.put(reverse('get_states_with_pk', kwargs={'nm': 'id', 'pk': state_pk}), data=data,
                                   content_type='application/json')
        state_obj = State.objects.get(pk=state_pk)
        serializer = StateSerializer(state_obj)
        self.assertEqual(response.data, self.read_state_serializer(serializer))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_state_with_pk_invalid(self):
        data = json.dumps({'titlee': 'astrology'})
        state_pk = self.state.pk
        response = self.client.put(reverse('get_states_with_pk', kwargs={'nm': 'id', 'pk': state_pk}), data=data,
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_state_with_params_valid(self):
        state_id = self.state.id - 1
        response = self.client.delete(reverse('get_states_with_params')+f'?id={state_id}',# {'id': state_id},
                                      content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_state_with_params_invalid(self):
        state_id = self.state.id + 1
        response = self.client.delete(reverse('get_states_with_params')+f'?id={state_id}',
                                      content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.client.delete(reverse('get_states_with_params'),
                                      content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_state_with_pk_valid(self):
        state_pk = self.state.pk - 1
        response = self.client.delete(reverse('get_states_with_pk', kwargs={'nm': 'id', 'pk': state_pk}),
                                      content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_state_with_pk_invalid(self):
        state_pk = self.state.pk + 1
        response = self.client.delete(reverse('get_states_with_pk', kwargs={'nm': 'id', 'pk': state_pk}),
                                      content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all_state_by_author_with_params_valid(self):
        author = ['author', 4]
        response = self.client.get(reverse('get_states_with_params') + f'?{author[0]}={author[1]}')
        author = State.objects.filter(**{author[0]: author[1]})
        author_serializer = StateSerializer(author, many=True)
        self.assertEqual(response.data, self.read_state_serializer(author_serializer))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_state_by_author_with_params_invalid(self):
        author = ['author', 50]
        response = self.client.get(reverse('get_states_with_params') + f'?{author[0]}={author[1]}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all_state_by_author_with_pk_valid(self):
        author = ['author', 4]
        response = self.client.get(reverse('get_states_with_pk', kwargs={'nm': author[0], 'pk': author[1]}))
        author = State.objects.filter(**{author[0]: author[1]})
        author_serializer = StateSerializer(author, many=True)
        self.assertEqual(response.data, self.read_state_serializer(author_serializer))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_state_by_author_with_pk_invalid(self):
        author = ['author', 50]
        response = self.client.get(reverse('get_states_with_pk', kwargs={'nm': author[0], 'pk': author[1]}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_all_state_by_author_with_params_valid(self):
        author = ['author', 4]
        response = self.client.delete(reverse('get_states_with_params') + f'?{author[0]}={author[1]}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_all_state_by_author_with_params_invalid(self):
        author = ['author', 10]
        response = self.client.delete(reverse('get_states_with_params') + f'?{author[0]}={author[1]}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_all_state_by_author_with_pk_valid(self):
        author = ['author', 4]
        response = self.client.delete(reverse('get_states_with_pk', kwargs={'nm': author[0], 'pk': author[1]}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_all_state_by_author_with_pk_invalid(self):
        author = ['author', 10]
        response = self.client.delete(reverse('get_states_with_pk', kwargs={'nm': author[0], 'pk': author[1]}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all_state_by_tag_with_params_valid(self):
        tag = ['tag', 4]
        response = self.client.get(reverse('get_states_with_params') + f'?{tag[0]}={tag[1]}')
        tag = State.objects.filter(**{tag[0]: tag[1]})
        tag_serializer = StateSerializer(tag, many=True)
        self.assertEqual(response.data, self.read_state_serializer(tag_serializer))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_state_by_tag_with_params_invalid(self):
        tag = ['tag', 3]
        response = self.client.get(reverse('get_states_with_params') + f'?{tag[0]}={tag[1]}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_state_by_tag_with_pk_valid(self):
        tag = ['tag', 4]
        response = self.client.get(reverse('get_states_with_pk', kwargs={'nm': tag[0], 'pk': tag[1]}))
        tag = State.objects.filter(**{tag[0]: tag[1]})
        tag_serializer = StateSerializer(tag, many=True)
        self.assertEqual(response.data, self.read_state_serializer(tag_serializer))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_state_by_tag_with_pk_invalid(self):
        tag = ['tag', 3]
        response = self.client.get(reverse('get_states_with_pk', kwargs={'nm': tag[0], 'pk': tag[1]}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_all_state_by_tag_with_params_valid(self):
        tag = ['tag', 4]
        response = self.client.delete(reverse('get_states_with_params') + f'?{tag[0]}={tag[1]}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_all_state_by_tag_with_params_invalid(self):
        tag = ['tag', 40]
        response = self.client.delete(reverse('get_states_with_params') + f'?{tag[0]}={tag[1]}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_all_state_by_tag_with_pk_valid(self):
        tag = ['tag', 4]
        response = self.client.delete(reverse('get_states_with_pk', kwargs={'nm': tag[0], 'pk': tag[1]}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_all_state_by_tag_with_pk_invalid(self):
        tag = ['tag', 40]
        response = self.client.delete(reverse('get_states_with_pk', kwargs={'nm': tag[0], 'pk': tag[1]}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all_state_by_category_with_params_valid(self):
        category = ['category', 4]
        response = self.client.get(reverse('get_states_with_params') + f'?{category[0]}={category[1]}')
        state = State.objects.filter(**{category[0]: category[1]})
        state_serializer = StateSerializer(state, many=True)
        self.assertEqual(response.data, self.read_state_serializer(state_serializer))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_state_by_category_with_params_invalid(self):
        category = ['category', 50]
        response = self.client.get(reverse('get_states_with_params') + f'?{category[0]}={category[1]}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all_state_by_category_with_pk_valid(self):
        category = ['category', 4]
        response = self.client.get(reverse('get_states_with_pk', kwargs={'nm': category[0], 'pk': category[1]}))
        state = State.objects.filter(**{category[0]: category[1]})
        state_serializer = StateSerializer(state, many=True)
        self.assertEqual(response.data, self.read_state_serializer(state_serializer))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_state_by_category_with_pk_invalid(self):
        category = ['category', 50]
        response = self.client.get(reverse('get_states_with_pk', kwargs={'nm': category[0], 'pk': category[1]}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_all_state_by_category_with_params_valid(self):
        category = ['category', 4]
        response = self.client.delete(reverse('get_states_with_params') + f'?{category[0]}={category[1]}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_all_state_by_category_with_params_invalid(self):
        category = ['category', 50]
        response = self.client.delete(reverse('get_states_with_params') + f'?{category[0]}={category[1]}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_all_state_by_category_with_pk_valid(self):
        category = ['category', 4]
        response = self.client.delete(reverse('get_states_with_pk', kwargs={'nm': category[0], 'pk': category[1]}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_all_state_by_category_with_pk_invalid(self):
        category = ['category', 50]
        response = self.client.delete(reverse('get_states_with_pk', kwargs={'nm': category[0], 'pk': category[1]}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all_state_by_date_with_params_valid(self):
        date = ['date', '2022-01-14']
        response = self.client.get(reverse('get_states_with_params') + f'?{date[0]}={date[1]}')
        state = State.objects.filter(**{date[0]: date[1]})
        state_serializer = StateSerializer(state, many=True)
        self.assertEqual(response.data, self.read_state_serializer(state_serializer))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_state_by_date_with_params_invalid(self):
        date = ['date', '2222-01-14']
        response = self.client.get(reverse('get_states_with_params') + f'?{date[0]}={date[1]}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all_state_by_date_with_pk_valid(self):
        date = ['date', '2022-01-14']
        response = self.client.get(reverse('get_states_with_pk', kwargs={'nm': date[0], 'pk': date[1]}))
        state = State.objects.filter(**{date[0]: date[1]})
        state_serializer = StateSerializer(state, many=True)
        self.assertEqual(response.data, self.read_state_serializer(state_serializer))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_state_by_date_with_pk_invalid(self):
        date = ['date', '2222-01-14']
        response = self.client.get(reverse('get_states_with_pk', kwargs={'nm': date[0], 'pk': date[1]}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_all_state_by_date_with_params_valid(self):
        date = ['date', '2022-01-14']
        response = self.client.delete(reverse('get_states_with_params') + f'?{date[0]}={date[1]}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_all_state_by_date_with_params_invalid(self):
        date = ['date', '2222-01-14']
        response = self.client.delete(reverse('get_states_with_params') + f'?{date[0]}={date[1]}')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_all_state_by_date_with_pk_valid(self):
        date = ['date', '2022-01-14']
        response = self.client.delete(reverse('get_states_with_pk', kwargs={'nm': date[0], 'pk': date[1]}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_all_state_by_date_with_pk_invalid(self):
        date = ['date', '2222-01-14']
        response = self.client.delete(reverse('get_states_with_pk', kwargs={'nm': date[0], 'pk': date[1]}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
