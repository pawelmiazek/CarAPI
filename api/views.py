from django.shortcuts import render
from django.db.models import Count

from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CarSerializer, PopularSerializer, RateSerializer

from .models import Car, Rate


@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'Car List & Car Create': '/cars/',
        'Popular List': '/popular/',
        'Rate Create': '/rate/'
    }
    return Response(api_urls)


class CarListCreate(generics.ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
        

class RateCreate(generics.CreateAPIView):
    serializer_class = RateSerializer


class PopularView(APIView):
    def get(self, request, format=None, **kwargs):
        car = Car.objects.annotate(rates=Count('rate_set')).order_by('-rates')
        serializer = PopularSerializer(car, many=True)
        return Response(serializer.data)
