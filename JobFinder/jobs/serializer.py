from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Offer

# Offer serializer
class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'