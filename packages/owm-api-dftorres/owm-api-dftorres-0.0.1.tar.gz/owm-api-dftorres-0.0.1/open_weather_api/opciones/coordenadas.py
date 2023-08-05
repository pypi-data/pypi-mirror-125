from api import Api


class Coordenadas(Api):

    def __init__(self, config=None, latitud=None, longitud=None):
        if latitud == '' or latitud == None or longitud == '' or longitud == None:
            raise ValueError('Se requiere latitud y longitud')

        if config == None:
            raise ValueError('Configuración requerida')

        self.set_latitud(latitud)
        self.set_longitud(longitud)
        super().__init__(config)

    def set_latitud(self, latitud):
        self.__latitud = latitud

    def get_latitud(self):
        return self.__latitud

    def set_longitud(self, longitud):
        self.__longitud = longitud

    def get_longitud(self):
        return self.__longitud

    def get_data(self):
        return super().get_data('lat={}&lon={}'.format(self.__latitud, self.__longitud))
