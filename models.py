from peewee import *
import datetime


# db = SqliteDatabase('datos.db')
db = MySQLDatabase('si_oti', user='root', password='', host='127.0.0.1', port=3306)


###############################################################################
# CharField
#   default max_length=255

###############################################################################

class BaseModel(Model):
    class Meta:
        database = db

###############################################################################
###############################################################################
###############################################################################

# ok
class Modalidad(BaseModel):
    id = AutoField()
    nombre = CharField()

# ok
class EstadoDelBien(BaseModel):
    id = AutoField()
    nombre = CharField(null=False)

# ok
class Ubicacion(BaseModel):
    id = AutoField()
    nombre = CharField(null=False)

class Personal(BaseModel):
    '''
    Personal
    Contendra personal que labora en la universidad que puede estar a 
    cargo(responsable) de bienes relacionados con la OTI.
    ciet
    '''
    id = AutoField()
    nombres = CharField(null=False)
    apellido_paterno = CharField(null=False)
    apellido_materno = CharField(null=False)
    modalidad = ForeignKeyField(Modalidad) # unique ? ...

    area_dependencia = CharField(default='')
    
    # correo = CharField()
    # telefono = CharField()

    # codigo = CharField()
    # cargo = CharField()


###############################################################################
###############################################################################
###############################################################################


class Usuario(BaseModel):
    '''
    Usuario
    
    Props:
        estado: valor bool, indica si la cuenta del usuario esta habilitada para logearse.
    '''
    id = AutoField()
    username = CharField(unique=True, null=False)
    contrasena = CharField(null=False)

    nombres = CharField(unique=True, null=False)
    apellido_paterno = CharField(null=False)
    apellido_materno = CharField(null=False)
    # jefe o personal
    is_admin = BooleanField(null=False)
    # usuario habilitado o deshabilitado para acceder al sistema
    habilitado = BooleanField(null=False, default=True)


    def __repr__(self):
        return '{} {} {} {} {} {}'.format(self.username, self.nombres, self.apellido_paterno, self.apellido_materno, self.is_admin, self.habilitado)

    

    # def __str__(self):
    #     self.nick = self.nick.title()



class Bien(BaseModel):
    '''Esta clase representa los bienes que se registraran en la base de datos
    
    '''
    id = AutoField()
    denominacion = CharField(null=False)
    numero_serie = CharField(null=False, default='Sin serie')
    numero_patrimonial = CharField(null=False, default='Sin código')
    # bueno regular malogrado malo

    estado = ForeignKeyField(EstadoDelBien, null=False)
    marca = CharField(default='')
    ubicacion = ForeignKeyField(Ubicacion, null=False)
    # puede ser sin inventario...entonces sera '' lo cual se traduce en 
    # ser un camṕo de tipo charfield
    descripcion = TextField(default='')
    # TODO 
    # analise
    ultimo_inventario = CharField(null=False, default='Sin inventario')



class Suceso(BaseModel):
    """ Este modelo alamacena eventos que pueden suceder con el bien,
    mantenimiento reparacion.

        Ejemplo:
            Mantenimineto
            Reparacion
            Otro
            ...

            fecha en la que sucedio
            y fecha de registrado el incidente
        """
    id = AutoField()
    # tipo de suceso, reparacion, mantenimiento, otro
    tipo = CharField(null=False)
    descripcion = TextField(null=False, default='')

    fecha_del_suceso = DateField()
    fecha_registrada = DateTimeField(null=False, default=datetime.datetime.now)


    usuario_que_registro = ForeignKeyField(Usuario, null=False)
    bien = ForeignKeyField(Bien)
    # estado = CharField()


class Historial(BaseModel):
    """ En este modelo se guardara el historial de modificaciones que se realize
    al bien.

    Este modelo tendra todos los campos modificables(que pueden cambiar en el bien) de BIEN

    Ejemplo:
        Cambio de lugar
        Cambio de responsable
        ...

    """
    id = AutoField()
    # cambio de ubicacion
    ubicacion = ForeignKeyField(Ubicacion, null=False)
    # cambio de responsable
    responsable = ForeignKeyField(Personal, null=False)
    fecha_del_suceso = DateField(null=False, default=datetime.date.today)
    fecha_registrada = DateTimeField(null=False, default=datetime.datetime.today)
    
    bien = ForeignKeyField(Bien)
    # estado = CharField()


class Acta(BaseModel):
    '''Acta

    Sera una tabla para reportar...
    '''
    id = AutoField()
    transferente = ForeignKeyField(Personal, null=False)
    receptor = ForeignKeyField(Personal, null=False)
    observaciones = TextField(default='')
    fecha = DateField(null=False, default=datetime.date.today)

    bienes = ForeignKeyField(Bien)



###############################################################################
###############################################################################
###############################################################################

# # ok
# class Estado(BaseModel):
#     denominacion = CharField(max_length=256, null=False)


class Switch(BaseModel):
    id = AutoField()
    denominacion = CharField(null=False)
    numero_serie = CharField(null=False)
    numero_patrimonial = CharField(null=False)
    cantidad_de_puertos = IntegerField(null=False, default=0)
    puertos_en_uso = IntegerField(null=False, default=0)
    puertos_libres = IntegerField(default=cantidad_de_puertos-puertos_en_uso, null=False)
    configurable = BooleanField(null=False, default=False)
    red = CharField(null=False)
    tipo = CharField(null=False)
    marca = CharField(null=False)
    descripcion = CharField()


# class UPS(BaseModel):
#     # tipo de suceso, reparacion, mantenimiento, otro
#     denominacion = CharField(max_length=512, null=False)
#     numero_serie = CharField(max_length=512, null=False)
#     numero_patrimonial = CharField(max_length=512, null=False)
#     marca = CharField(max_length=512, null=False)



# class AdaptadorTelefonico(BaseModel):
#     # tipo de suceso, reparacion, mantenimiento, otro
#     denominacion = CharField(max_length=512, null=False)
#     numero_serie = CharField(max_length=512, null=False)
#     numero_patrimonial = CharField(max_length=512, null=False)

# class AdaptadorTelefonico(BaseModel):
#     # tipo de suceso, reparacion, mantenimiento, otro
#     denominacion = CharField(max_length=512, null=False)
#     numero_serie = CharField(max_length=512, null=False)
#     numero_patrimonial = CharField(max_length=512, null=False)

###############################################################################



'''

viendo lo complejo que puede ser se trato de simplificar a estas 
tablas

asumiendo que los bienes estan en un gabinete

se necesita una tabla gabinete adicional...

tomar en cuenta que en la ubicacion puede ponerse tambien direccion ya que
tambien se registrara equipos de Derecho, Edificio de educacion continua

Una tabla para switch
Una tabla para PDU
Una tabla para switch
Una tabla para switch


la facu, lugar tiene(Entidad) 
    (list entities)
    gabinete(entidad)
        Switch(entidad)
        ordenador de cable(entidad)
    pdu(entidad)
    otros(entidad)

que es lo mas inportante en un gabinete ???
...

'''


#################################################################################


###############################################################################



if __name__ == '__main__':
    db.connect()



    # db.drop_tables(
    # [
    #     Modalidad,
    #     EstadoDelBien,
    #     Ubicacion,
    #     Personal,
    #     Usuario,
    #     Bien,
    #     Suceso,
    #     Historial,
    #     Acta
    # ])

    db.create_tables(
    [
        Modalidad,
        EstadoDelBien,
        Ubicacion,
        Personal,
        Usuario,
        Bien,
        Suceso,
        Historial,
        Acta
    ])

    Modalidad.create(nombre='Funcionario')
    Modalidad.create(nombre='Nombrado')
    Modalidad.create(nombre='Contrato por planilla')
    Modalidad.create(nombre='CAS')

    EstadoDelBien.create(nombre='Bueno')
    EstadoDelBien.create(nombre='Malo')
    EstadoDelBien.create(nombre='Regular')
    EstadoDelBien.create(nombre='Inservible')

    db.close()

