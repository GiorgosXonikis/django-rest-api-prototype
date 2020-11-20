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
    Class to POST and Predict Home Price
    """

    @staticmethod
    def get(request):
        _district = request.query_params['district']
        _rooms = request.query_params['rooms']
        _size = request.query_params['size']

        return Response(
            {
                "estimated_price": util.get_estimated_price(_district, _rooms, _size)
            },
            status=status.HTTP_200_OK
        )
