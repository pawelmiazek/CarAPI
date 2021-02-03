from rest_framework import serializers
from .models import Car, Rate
import requests


class CarSerializer(serializers.ModelSerializer):

    class Meta:
        model = Car
        fields = '__all__'
        read_only_fields = ('average_rate',)
    
    average_rate = serializers.SerializerMethodField()

    def get_average_rate(self, obj):
        rates = [item.rate for item in Rate.objects.filter(car=obj)]
        average_rate = sum(rates) if rates else 0
        return average_rate
    
    def create(self, validated_data):
        make_name = validated_data.get('make')
        model_name = validated_data.get('model')
        r = requests.get(
            'https://vpic.nhtsa.dot.gov/api/vehicles/getallmakes?format=json'
        )
        make_results = r.json()['Results']
        search_make = [
            make for make in make_results if make.get('Make_Name').upper() == make_name.upper()
        ]
        if len(search_make) == 0:
            raise serializers.ValidationError(
                "The specified car make does not exist."
            )
        else:
            r = requests.get(
                f'https://vpic.nhtsa.dot.gov/api/vehicles/getmodelsformake/{make_name.lower()}?format=json'
            )
            model_results = r.json()['Results']
            search_model = [
                model for model in model_results if model.get('Model_Name').upper() == model_name.upper()
            ]
            if len(search_model) == 0:
                raise serializers.ValidationError(
                    "The specified car model does not exist."
                )
            else:
                return Car.objects.create(**validated_data)



class PopularSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'
        read_only_fields = ('number_of_rates',)
    
    number_of_rates = serializers.SerializerMethodField()

    def get_number_of_rates(self, obj):
        number_of_rates = Rate.objects.filter(car=obj).count()
        return number_of_rates


class RateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rate
        fields = '__all__'
