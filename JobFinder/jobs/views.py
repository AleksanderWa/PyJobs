from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Offer
from .serializer import OfferSerializer
from .WebScraper import Parser
class JobsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

    def list(self, request, *args, **kwargs):


        parser = Parser()
        jobs = ["Python"]
        parser.get_data_from_pracuj_pl("Szczecin", *jobs)

        queryset = Offer.objects.all()

        serializer = OfferSerializer(queryset, many=True)
        return Response(serializer.data)