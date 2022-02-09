from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

class Car(models.Model):
    make = models.ForeignKey("Manufacturer", related_name='make', on_delete=models.CASCADE)
    model = models.CharField(max_length=250)

    def __str__(self):
        return "%s %s" % (self.make, self.model)


class Manufacturer(models.Model):
    manufacturer_name = models.CharField(max_length=250)

    def __str__(self):
        return self.manufacturer_name


class Rate(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return "%s %s" % (self.car, self.rating)
