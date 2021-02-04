from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Car, Rate
from django.contrib.auth.models import User

class GetAllCarsTest(APITestCase):

    def setUp(self):
        Car.objects.create(make="make_1", model="model_1")
        Car.objects.create(make="make_2", model="model_2")
        Car.objects.create(make="make_3", model="model_3")
        Car.objects.create(make="make_4", model="model_4")

    def test_car_list(self):
        url = reverse('api:car-list-create')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateNewCarTest(APITestCase):
    
    def setUp(self):
        Car.objects.create(make="HONDA", model="METROPOLITAN")
        self.valid_data = {
            'make': 'HONDA',
            'model': 'Civic'
        }
        self.invalid_make = {
            'make': 'make',
            'model': 'Civic'
        }
        self.invalid_model = {
            'make': 'HONDA',
            'model': 'model'
        }
        self.not_unique_car = {
            'make': 'HONDA',
            'model': 'METROPOLITAn'
        }
        self.url = reverse('api:car-list-create')
    
    def test_create_valid_data(self):
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_invalid_make(self):
        response = self.client.post(self.url, self.invalid_make, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_model(self):
        response = self.client.post(self.url, self.invalid_model, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_not_unique_car(self):
        response = self.client.post(self.url, self.not_unique_car, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PopularTests(APITestCase):

    def setUp(self):
        car_1 = Car.objects.create(make="make1", model="model1")
        car_2 = Car.objects.create(make="make2", model="model2")
        Rate.objects.create(car=car_1, rate=1)
        Rate.objects.create(car=car_1, rate=2)
        Rate.objects.create(car=car_1, rate=3)
        Rate.objects.create(car=car_2, rate=4)
        Rate.objects.create(car=car_2, rate=5)

    def test_car_list(self):
        url = reverse('api:popular-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class RateTests(APITestCase):

    def setUp(self):
        car = Car.objects.create(make="make", model="model")
        self.valid_data = {
            'car': car.id,
            'rate': 3
        }
        self.invalid_data = {
            'make': car.id,
            'model': 7
        }
        self.url = reverse('api:rate-create')

    def test_create_valid_data(self):
        response = self.client.post(self.url, self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_data(self):
        response = self.client.post(self.url, self.invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
