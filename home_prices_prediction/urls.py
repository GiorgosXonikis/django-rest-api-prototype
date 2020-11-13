from django.urls import path

from home_prices_prediction.views import GetLocationNames, PredictHomePrice

urlpatterns = [
    path('location-names', GetLocationNames.as_view(), name='location-names'),
    path('predict-home-price', PredictHomePrice.as_view(), name='predict-home-price'),

]