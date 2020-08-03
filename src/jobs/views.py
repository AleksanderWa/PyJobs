from django.shortcuts import render
from django.views.generic import View
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
        jobs = ["full%20stack"]
        jobs_pracuj = parser.get_data_from_pracuj_pl("Szczecin", *jobs)

        queryset = Offer.objects.all()

        serializer = OfferSerializer(queryset, many=True)
        return Response(jobs_pracuj)


class MainPageView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "pages/front-end-render.html", {})