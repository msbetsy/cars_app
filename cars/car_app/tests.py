from django.test import TestCase
from .models import Manufacturer, Car, Rate


# Create your tests here.


class ManufacturerTest(TestCase):
    """ Test module for Manufacturer model """

    def setUp(self):
        Manufacturer.objects.create(manufacturer_name='Audi')
        Manufacturer.objects.create(manufacturer_name='Volvo')

    def test_manufacturer_str(self):
        manufacturer_audi = Manufacturer.objects.get(manufacturer_name='Audi')
        manufacturer_volvo = Manufacturer.objects.get(manufacturer_name='Volvo')
        self.assertEqual(str(manufacturer_audi), "Audi")
        self.assertEqual(str(manufacturer_volvo), "Volvo")


class CarTest(TestCase):
    """ Test module for Car model """

    def setUp(self):
        Manufacturer.objects.create(manufacturer_name='Audi')
        manufacturer_audi = Manufacturer.objects.get(manufacturer_name='Audi')
        Car.objects.create(model='A4', make=manufacturer_audi)

    def test_car_str(self):
        manufacturer_audi = Manufacturer.objects.get(manufacturer_name='Audi')
        car_audi = Car.objects.get(model='A4', make=manufacturer_audi.id)
        self.assertEqual(str(car_audi), "Audi A4")


class RateTest(TestCase):
    """ Test module for Rate model """

    def setUp(self):
        Manufacturer.objects.create(manufacturer_name='Audi')
        manufacturer_audi = Manufacturer.objects.get(manufacturer_name='Audi')
        car_audi = Car.objects.create(model='A4', make=manufacturer_audi)
        Rate.objects.create(car=car_audi, rating=4)

    def test_rate_str(self):
        manufacturer_audi = Manufacturer.objects.get(manufacturer_name='Audi')
        car_audi = Car.objects.get(model='A4', make=manufacturer_audi)
        rate_audi = Rate.objects.get(car=car_audi, rating=4)
        self.assertEqual(str(rate_audi), "Audi A4 4")
