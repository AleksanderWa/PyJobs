import json
from pprint import pprint

from bs4 import BeautifulSoup
from collections import namedtuple
from urllib.request import Request, urlopen
import logging

# from .models import Offer
from jobs.models import Offer


class Parser:
    # api-endpoint
    URL = "https://www.pracuj.pl/praca/"
    # "https://www.pracuj.pl/praca/python;kw/szczecin;wp"
    kw_separator = "-x44"
    PARAMS = namedtuple('Params', 'kw wp kw_sep')
    qr_params = PARAMS(';kw', ';wp', '-x44-')

    def parse_url(self, response):
        soup = BeautifulSoup(response, features="lxml")
        elements = soup.find_all("script", type="application/ld+json")
        print(len(elements))
        # breakpoint()
        # return True
        response_data = [
            self.create_job_json_ob(json.loads(offer.contents[0])) for offer in elements
        ]
        return response_data

    def compose_url(self, city, jobs):
        composed_url = self.URL
        if len(jobs)==1:
            composed_url = f"{self.URL}/{jobs[0]}{self.qr_params.kw}/{city}{self.qr_params.wp}"
        elif len(jobs) > 1:
            sufixes = [f"{each}{self.qr_params.kw_sep}" for each in jobs]
            suffixes_str = "".join(sufixes)
            composed_url = f"{self.URL}{suffixes_str}{self.qr_params.kw}/{city}{self.qr_params.wp}"

        return composed_url

    def get_data_from_pracuj_pl(self, city, *jobs):
        url = self.compose_url(city, jobs)

        print(f"URL : {url}")
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urlopen(req) as response:
            readable_data = self.parse_url(response)

            webpage = response.read()
        return readable_data

    def create_job_json_ob(self, data):

        offer_name = data['title']
        company = data['hiringOrganization']['name']
        publication_date = data['datePosted']
        offer_desc = data['description']
        location = data['jobLocation']['address']['addressLocality']
        Offer.objects.get_or_create(
            name=offer_name,
            company=company,
            description=offer_desc,
            publication_date=publication_date.split(':')[-1],
            city=location,
        )
        json_obj = {
            'name': offer_name,
            'company': company,
            'description': offer_desc,
            'publication_date': publication_date.split(':')[-1],
            'city': location,
        }
        return json_obj
#
#
# parser = Parser()
# jobs = ["python"]
# pprint(parser.get_data_from_pracuj_pl("gdansk", *jobs))
