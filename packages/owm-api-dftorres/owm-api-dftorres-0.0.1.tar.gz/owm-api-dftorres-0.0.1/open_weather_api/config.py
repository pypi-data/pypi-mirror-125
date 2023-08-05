from constantes import ACTUAL, PREVISION


class Config:

    def __init__(self, config):
        self.set_api_key(config['key'])
        self.set_units(config['units'])
        self.set_lang(config['lang'])
        self.set_type(config['type'])

    def set_api_key(self, key):
        if key == '' or key == None:
            raise ValueError('Debes especificar un api key')
        self.__api_key = f'&appid={key}'

    def get_api_key(self):
        return self.__api_key

    # Si no se recibe celcius (El que deseamos en nuestro caso)
    # dejamos vacio para que tome el por defecto, que es kelvin.
    def set_units(self, units):
        self.__units = '&units=metric' if units == 'metric' else ''

    def get_units(self):
        return self.__units

    # por defecto se deja inglés, si no, el que pasen.
    def set_lang(self, lang):
        self.__lang = '&lang={}'.format('en' if lang == '' or lang == None else lang)

    def get_lang(self):
        return self.__lang

    def set_type(self, type):
        if type != ACTUAL and type != PREVISION:
            raise ValueError('Debe especificar un tipo correcto. Actual o Prevision')
        self.__type = type

    def get_type(self):
        return self.__type
