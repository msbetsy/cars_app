from collections import OrderedDict
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from ...models import Car, Rate, Manufacturer


class RateTest(APITestCase):

    def setUp(self):
        self.manufacturer = Manufacturer.objects.create(manufacturer_name="Audi")
        self.car = Car.objects.create(make=self.manufacturer, model='A4')
        self.url = reverse('car_app_api:post_rate')
        Rate.objects.create(car_id=self.car.id, rating=1)

    def test_post_rate_201(self):
        data = {
            'car_id': self.car.id,
            'rating': 1
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_rate_400_car(self):
        data = {
            'car_id': self.car.id + 1,
            'rating': 1
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.data
        self.assertEqual(response_data["error"], "car doesn't exist")

    def test_post_rate_400_rating(self):
        data = {
            'car_id': self.car.id + 1,
            'rating': 6
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.data
        self.assertEqual(response_data["error"], "rating must be <1,5>")

    def test_post_rate_400_type(self):
        data = {
            'car_id': self.car.id + 1,
            'rating': "6"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.data
        self.assertEqual(response_data["wrong content type"], 'must be int')

    def test_post_rate_400_request(self):
        data = {
            'car_id': self.car.id + 1
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.data
        self.assertEqual(response_data["wrong request"], "must have: car_id, rating")


class PopularCarsTest(APITestCase):

    def setUp(self):
        self.manufacturer_audi = Manufacturer.objects.create(manufacturer_name="Audi")
        self.car_a4 = Car.objects.create(make=self.manufacturer_audi, model='A4')
        Rate.objects.create(car_id=self.car_a4.id, rating=5)
        self.manufacturer_seat = Manufacturer.objects.create(manufacturer_name="Kia")
        self.car_ibiza = Car.objects.create(make=self.manufacturer_seat, model='Cadenza')
        Rate.objects.create(car_id=self.car_ibiza.id, rating=4)
        Rate.objects.create(car_id=self.car_ibiza.id, rating=5)
        Rate.objects.create(car_id=self.car_ibiza.id, rating=2)
        self.url = reverse('car_app_api:get_popular')

    def test_get_rate_200(self):
        response = self.client.get(self.url)
        data = [
            OrderedDict([
                ("id", self.car_ibiza.id),
                ("model", "Cadenza"),
                ("make", "Kia"),
                ("rates_number", 3)
            ]),
            OrderedDict([
                ("id", self.car_a4.id),
                ("model", "A4"),
                ("make", "Audi"),
                ("rates_number", 1)
            ])
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)


class CarsTest(APITestCase):

    def setUp(self):
        self.manufacturer_audi = Manufacturer.objects.create(manufacturer_name="Audi")
        self.car_a4 = Car.objects.create(make=self.manufacturer_audi, model='A4')
        Rate.objects.create(car_id=self.car_a4.id, rating=5)
        Rate.objects.create(car_id=self.car_a4.id, rating=1)
        self.manufacturer_seat = Manufacturer.objects.create(manufacturer_name="Kia")
        self.car_ibiza = Car.objects.create(make=self.manufacturer_seat, model='Cadenza')
        self.url = reverse('car_app_api:car_list')

    def test_get_cars_200(self):
        response = self.client.get(self.url)
        data = [OrderedDict([
            ("id", self.car_a4.id),
            ("model", "A4"),
            ("make", "Audi"),
            ("avg_rating", 3.0)
        ]),
            OrderedDict([
                ("id", self.car_ibiza.id),
                ("model", "Cadenza"),
                ("make", "Kia"),
                ("avg_rating", None)
            ])
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)

    def test_post_cars_400_request(self):
        data = {
            'make': 'Kia'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.data
        self.assertEqual(response_data["wrong request"], "must have: make, model")

    def test_post_cars_400_type(self):
        data = {
            'make': 'Kia',
            'model': 5
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response_data = response.data
        self.assertEqual(response_data["wrong content type"], "must be str")

    def test_post_cars_404_manufacturer(self):
        data = {
            'make': 'Kia2',
            'model': 'Cadenza'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response_data = response.data
        self.assertEqual(response_data["error"], "manufacturer doesn't exist")

    def test_post_cars_404_model(self):
        data = {
            'make': 'Kia',
            'model': 'Cadenza2'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response_data = response.data
        self.assertEqual(response_data["error"], "model doesn't exist")

    def test_post_cars_200(self):
        data = {
            'make': 'opel',
            'model': 'roadster'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Manufacturer.objects.filter(manufacturer_name="Opel").first().manufacturer_name, "Opel")
        make = Manufacturer.objects.filter(manufacturer_name="Opel").first()
        self.assertEqual(Car.objects.filter(make=make, model='Roadster').first().model, "Roadster")


class CarsDeleteTest(APITestCase):

    def setUp(self):
        self.manufacturer_audi = Manufacturer.objects.create(manufacturer_name="Audi")
        self.car_a4 = Car.objects.create(make=self.manufacturer_audi, model='A4')

    def test_delete_cars_200(self):
        url = reverse('car_app_api:car_delete', kwargs={"car_id": 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(Car.objects.all()), 0)

    def test_delete_cars_400(self):
        url = reverse('car_app_api:car_delete', kwargs={"car_id": 10})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "car doesn't exist")
