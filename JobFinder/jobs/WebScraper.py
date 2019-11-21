from bs4 import BeautifulSoup
from collections import namedtuple
import logging
import requests

from .models import Offer


class Parser:
    # api-endpoint
    URL = "https://www.pracuj.pl/praca/"
    # "https://www.pracuj.pl/praca/python;kw/szczecin;wp"
    kw_separator = "-x44"
    PARAMS = namedtuple('Params', 'kw wp kw_sep')
    qr_params = PARAMS(';kw', ';wp', '-x44-')

    def parse_url(self, data):
        soup = BeautifulSoup(data, features="html.parser")
        elements = soup.findAll("li", class_="results__list-container-item")

        for offer in elements:
            offer_name = offer.find("h3", class_="offer-details__title")
            company = offer.find("p", class_="offer-company")
            publication_date = offer.find("span", class_="offer-actions__date")
            offer_text = offer.find("span", class_="offer-description__content")

            offer_name = self.remove_empty_lines_from_html(offer_name)
            company = self.remove_empty_lines_from_html(company)
            publication_date = self.remove_empty_lines_from_html(publication_date)
            offer_text = self.remove_empty_lines_from_html(offer_text)

            Offer.objects.get_or_create(
                name=offer_name,
                company=company,
                offer_text=offer_text,
                publication_date=publication_date.split(':')[-1],
            )

            print(f"name : {offer_name}, company : {company}, publication: {publication_date.split(':')[-1]}, text : {offer_text}")
        return elements

    def compose_url(self, city, jobs):
        composed_url = self.URL
        if len(jobs) == 1:
            composed_url = f"{self.URL}/{jobs[0]}{self.qr_params.kw}/{city}{self.qr_params.wp}"
        elif len(jobs) > 1:
            sufixes = [f"{each}{self.qr_params.kw_sep}" for each in jobs]
            suffixes_str = "".join(sufixes)
            composed_url = f"{self.URL}{suffixes_str}{self.qr_params.kw}/{city}{self.qr_params.wp}"

        return composed_url

    def get_data_from_pracuj_pl(self, city, *jobs):
        url = self.compose_url(city, jobs)
        print(f"URL : {url}")
        r = requests.get(url=url)
        readable_data = self.parse_url(r.content)
        return readable_data

    def remove_empty_lines_from_html(self, html_code):
        formated = html_code.get_text().replace("\n", "")
        return formated


