import requests as request
from config import Config
from constantes import URL


class Api(Config):

    def __init__(self, config):
        super().__init__(config)

    def __get_url(self, find_params):
        lang = self.get_lang()
        units = self.get_units()
        api_key = self.get_api_key()
        params = f'{find_params}{lang}{units}{api_key}'
        url = f'{URL}{self.get_type()}{params}'
        return url

    def get_data(self, find_params):
        "Obtener los datos con la url generada"
        return request.get(self.__get_url(find_params)).json()
