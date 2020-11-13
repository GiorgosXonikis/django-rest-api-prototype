from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from home_prices_prediction import util


class GetLocationNames(APIView):
    """
    Class to GET Location names
    """

    @staticmethod
    def get(request):
        return Response(
            {
                "location_names": util.get_location_names()
            },
            status=status.HTTP_200_OK
        )


class PredictHomePrice(APIView):
    """
    Class to GET and Predict Home Price
    """

    @staticmethod
    def get(request):
        _location = request.data['suburb']
        _type = request.data['type']
        _rooms = request.data['rooms']

        return Response(
            {
                "estimated_price": util.get_estimated_price(_location, _type, _location)
            },
            status=status.HTTP_200_OK
        )
