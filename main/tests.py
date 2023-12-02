from django.test import TestCase
from datetime import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User, Coords, Level, Pereval, Images
from .serializers import PerevalSerializer


class PerevalApiTestCase(APITestCase):

    def setUp(self):
        user_1 = User.objects.create(email='ivanov@mail.ru', phone='+79101111111', fam='Иванов', name='Иван', otc='Иванович')
        user_2 = User.objects.create(email='petrov@mail.ru', phone='+79102222222', fam='Петров', name='Пётр', otc='Петрович')
        coords_1 = Coords.objects.create(latitude=11.1111, longitude=15.5555, height=1100)
        coords_2 = Coords.objects.create(latitude=12.2222, longitude=16.6666, height=1200)
        level_1 = Level.objects.create(winter='1a', spring='1a', summer='1a', autumn='1a')
        level_2 = Level.objects.create(winter='2a', spring='2a', summer='2a', autumn='2a')
        self.pereval_1 = Pereval.objects.create(add_time=datetime.now(), user=user_1, coords=coords_1, level=level_1,
                                beauty_title='beauty_title_1', title="title_1", other_titles='other_titles_1')
        self.pereval_2 = Pereval.objects.create(add_time=datetime.now(), user=user_2, coords=coords_2, level=level_2,
                                beauty_title='beauty_title_2', title="title_2", other_titles='other_titles_2')

    def test_get_list(self):
        url = reverse('pereval-list')
        response = self.client.get(url)
        print('response=', response)
        serializer_data = PerevalSerializer([self.pereval_1, self.pereval_2], many=True).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(len(serializer_data), 2)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_detail(self):
        url = reverse('pereval-detail', args=(self.pereval_1.id, ))
        response = self.client.get(url)
        serializer_data = PerevalSerializer(self.pereval_1).data
        self.assertEqual(serializer_data, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)


class PerevalSerializerTestCase(TestCase):

    def setUp(self):
        user_1 = User.objects.create(email='ivanov@mail.ru', phone='+79101111111', fam='Иванов', name='Иван', otc='Иванович')
        user_2 = User.objects.create(email='petrov@mail.ru', phone='+79102222222', fam='Петров', name='Пётр', otc='Петрович')
        coords_1 = Coords.objects.create(latitude=11.1111, longitude=15.5555, height=1100)
        coords_2 = Coords.objects.create(latitude=12.2222, longitude=16.6666, height=1200)
        level_1 = Level.objects.create(winter='1a', spring='1a', summer='1a', autumn='1a')
        level_2 = Level.objects.create(winter='2a', spring='2a', summer='2a', autumn='2a')
        self.pereval_1 = Pereval.objects.create(add_time=datetime.now(), user=user_1, coords=coords_1, level=level_1,
                                beauty_title='beauty_title_1', title="title_1", other_titles='other_titles_1')
        self.pereval_2 = Pereval.objects.create(add_time=datetime.now(), user=user_2, coords=coords_2, level=level_2,
                                beauty_title='beauty_title_2', title="title_2", other_titles='other_titles_2')

    def test_check(self):
        serializer_data = PerevalSerializer([self.pereval_1, self.pereval_2], many=True).data

        expected_data = [
            {
                "id": 1,
                "beauty_title": "beauty_title_1",
                "title": "title_1",
                "other_titles": "other_titles_1",
                "connect": None,
                "add_time": self.pereval_1.add_time.strftime("%Y-%m-%dT%H:%M:%S.%f"),
                "level": {
                    #"id": 1,
                    "winter": "1a",
                    "summer": "1a",
                    "autumn": "1a",
                    "spring": "1a"
                },
                "user": {
                    "email": "ivanov@mail.ru",
                    "phone": "+79101111111",
                    "fam": "Иванов",
                    "name": "Иван",
                    "otc": "Иванович"
                },
                "coords": {
                    "latitude": 11.1111,
                    "longitude": 15.5555,
                    "height": 1100
                },
                "images": [],
                "status": "new"
            },
            {
                "id": 2,
                "beauty_title": "beauty_title_2",
                "title": "title_2",
                "other_titles": "other_titles_2",
                "connect": None,
                "add_time": self.pereval_2.add_time.strftime("%Y-%m-%dT%H:%M:%S.%f"),
                "level": {
                    #"id": 2,
                    "winter": "2a",
                    "summer": "2a",
                    "autumn": "2a",
                    "spring": "2a"
                },
                "user": {
                    "email": "petrov@mail.ru",
                    "phone": "+79102222222",
                    "fam": "Петров",
                    "name": "Пётр",
                    "otc": "Петрович"
                },
                "coords": {
                    "latitude": 12.2222,
                    "longitude": 16.6666,
                    "height": 1200
                },
                "images": [],
                "status": "new"
            },
        ]

        # print(expected_data)
        # print('++++++++++++++++++++++++++++++')
        # print(serializer_data)

        self.assertEqual(serializer_data, expected_data)
