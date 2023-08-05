from api import Api


class Ciudad(Api):

    def __init__(self, config=None, ciudad=None):
        if ciudad == '' or ciudad == None:
            raise ValueError('Nombre de la ciudad requerido')

        if config == None:
            raise ValueError('Configuración requerida')

        self.set_nombre(ciudad)
        super().__init__(config)

    def set_nombre(self, ciudad):
        self.__nombre = ciudad

    def get_nombre(self):
        return self.__nombre

    def get_data(self):
        return super().get_data(f'q={self.__nombre}')
