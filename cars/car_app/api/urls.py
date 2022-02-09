from django.urls import path
from .views import car_list, car_delete_rest_endpoint, post_rate_rest_endpoint, get_popular_cars_rest_endpoint

app_name = 'car_app_api'

urlpatterns = [
    path('cars/', car_list, name="car_list"),
    path('cars/<int:car_id>/', car_delete_rest_endpoint, name="car_delete"),
    path('rate/', post_rate_rest_endpoint, name="post_rate"),
    path('popular/',get_popular_cars_rest_endpoint,name="get_popular")
]
