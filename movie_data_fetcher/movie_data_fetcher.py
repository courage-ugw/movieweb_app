import pprint

import requests


class MovieDataFetcher:

    def __init__(self):
        self._request_url = 'https://www.omdbapi.com/?apikey=eb462b7d&t='
        self._request_url_country = "https://rest-countries10.p.rapidapi.com/country/"
        self._headers = {
            "X-RapidAPI-Key": "9bcf117f10msh4043aa916958825p12243fjsnd31208cf6b30",
            "X-RapidAPI-Host": "rest-countries10.p.rapidapi.com"
        }

    def get_movies_data(self, movie_name):
        try:
            url = self._request_url + movie_name
            return requests.get(url).json()
        except KeyError:
            return None

    def get_country_alpha_code(self, country_name):
        try:
            url = self._request_url_country + country_name
            response = requests.get(url, headers=self._headers).json()
            return response[0]['code']['alpha3code']
        except KeyError:
            return None

        except IndexError:
            return None