from rest_framework import serializers
from django.db.models import Avg
from ..models import Car, Rate


class GetCarSerializer(serializers.HyperlinkedModelSerializer):
    make = serializers.StringRelatedField(many=False)
    avg_rating = serializers.SerializerMethodField()

    class Meta:
        model = Car
        fields = ("id", "model", "make", "avg_rating")
        read_only_fields = ('id', 'avg_rating')

    @staticmethod
    def get_avg_rating(car):
        rates = Rate.objects.filter(car=car.id)

        if rates:
            avg_rating_dict = rates.aggregate(Avg('rating'))
            avg_rating = round(avg_rating_dict['rating__avg'], 1)
            return avg_rating
        else:
            return None


class GetPopularCarSerializer(serializers.HyperlinkedModelSerializer):
    make = serializers.StringRelatedField(many=False)
    rates_number = serializers.IntegerField(read_only=True)

    class Meta:
        model = Car
        fields = ("id", "model", "make", "rates_number")
        read_only_fields = ('id', 'rates_number')
