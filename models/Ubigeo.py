class Departamento:
    def __init__(self,id_departamento,nombre):
        self.id_departamento = id_departamento
        self.nombre = nombre


######################
class Provincia:
    def __init__(self,id_provincia,nombre,id_departamento):
        self.id_provincia = id_provincia
        self.nombre = nombre
        self.id_departamento = id_departamento


######################
class Distrito:
    def __init__(self,id_distrito,nombre,id_provincia):
        self.id_distrito = id_distrito
        self.nombre = nombre
        self.id_provncia = id_provincia




