from bs4 import BeautifulSoup
from collections import namedtuple
import logging
import requests


class Parser:
    # api-endpoint
    URL = "https://www.pracuj.pl/praca/"
    # "https://www.pracuj.pl/praca/python;kw/szczecin;wp"
    kw_separator = "-x44"
    PARAMS = namedtuple('Params', 'kw wp kw_sep')
    qr_params = PARAMS(';kw', ';wp', '-x44-')

    def parse_url(self, data):
        soup = BeautifulSoup(data, features="html.parser")
        div = soup.find("div", class_="offer-details")
        # dict_results = [y.get_text().replace("\xa0", '') for (row, y) in enumerate(table.find_all('td')[8:]) if
        #                 row % 5 <= 2]

        return div

    def compose_url(self, city, jobs):
        print(f"jobs : {jobs}")
        print(f"type : {type(jobs)}")
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

parser = Parser()
jobs = ["Python", "Django"]
pracuj_pl_content = parser.get_data_from_pracuj_pl("Szczecin", *jobs)


print(pracuj_pl_content)