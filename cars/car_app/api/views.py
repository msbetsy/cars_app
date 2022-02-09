from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Count
import requests
from .serializers import GetCarSerializer, GetPopularCarSerializer
from ..models import Car, Manufacturer, Rate


# Create your views here.

@api_view(['GET', 'POST'])
def car_list(request):
    if request.method == 'GET':
        queryset = Car.objects.all()
        serializer_class = GetCarSerializer(queryset, many=True)
        return Response(serializer_class.data)

    elif request.method == 'POST':
        data = request.data
        if "make" in list(data.keys()) and "model" in list(data.keys()):
            if isinstance(data["make"], str) and isinstance(data["model"], str):
                manufacturer_name = data["make"].capitalize()
                car_model = data["model"].capitalize()
                url = f'https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{manufacturer_name}?format=json'
                car_data = requests.get(url).json()
                if car_data["Count"] != 0:
                    results = car_data["Results"]
                    for result in results:
                        if result["Model_Name"] == car_model:
                            make = Manufacturer.objects.filter(manufacturer_name=manufacturer_name).first()
                            if make is None:
                                new_make = Manufacturer(manufacturer_name=manufacturer_name)
                                new_make.save()
                            make = Manufacturer.objects.filter(manufacturer_name=manufacturer_name).first()
                            car = Car.objects.filter(make=make, model=car_model).first()
                            if not car:
                                new_car = Car(make=make, model=car_model)
                                new_car.save()
                            return Response(status=status.HTTP_200_OK)
                    content = {"error": "model doesn't exist"}
                    return Response(content, status=status.HTTP_404_NOT_FOUND)
                else:
                    content = {"error": "manufacturer doesn't exist"}
                    return Response(content, status=status.HTTP_404_NOT_FOUND)
            else:
                content = {'wrong content type': 'must be str'}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

        else:
            content = {'wrong request': 'must have: make, model'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def car_delete_rest_endpoint(request, car_id):
    try:
        car = Car.objects.get(id=car_id)
    except Car.DoesNotExist:
        content = {'error': "car doesn't exist"}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        car.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(["GET"])
def get_popular_cars_rest_endpoint(request):
    if request.method == 'GET':
        queryset = Car.objects.select_related("make") \
            .annotate(rates_number=Count('rate__rating')) \
            .order_by('-rates_number')
        serializer_class = GetPopularCarSerializer(queryset, many=True)
        return Response(serializer_class.data, status.HTTP_200_OK)


@api_view(["POST"])
def post_rate_rest_endpoint(request):
    data = request.data
    if "car_id" in list(data.keys()) and "rating" in list(data.keys()):
        car_id = data["car_id"]
        rating = data["rating"]
        if isinstance(car_id, int) and isinstance(rating, int):
            if 5 >= rating >= 1:
                try:
                    car = Car.objects.get(id=car_id)
                    new_rate = Rate(car=car, rating=rating)
                    new_rate.save()
                    return Response(status=status.HTTP_201_CREATED)
                except Car.DoesNotExist:
                    content = {'error': "car doesn't exist"}
                    return Response(content, status=status.HTTP_400_BAD_REQUEST)
            else:
                content = {'error': "rating must be <1,5>"}
                return Response(content, status=status.HTTP_400_BAD_REQUEST)

        else:
            content = {'wrong content type': 'must be int'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
    else:
        content = {'wrong request': 'must have: car_id, rating'}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
