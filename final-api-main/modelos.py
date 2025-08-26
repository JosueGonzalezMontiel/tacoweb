from peewee import *
from conexion import database


class Cliente(Model):
    cliente_id = AutoField(primary_key=True)
    nombre = CharField(max_length=100)
    numero = BigIntegerField()
    contrasena = CharField(max_length=100)

    class Meta:
        database = database
        table_name = 'cliente'


class Administrador(Model):
    admin_id = AutoField(primary_key=True)
    nombre = CharField(max_length=100)
    contrasena = CharField(max_length=100)

    class Meta:
        database = database
        table_name = 'administrador'


class Trabajador(Model):
    user_id = AutoField(primary_key=True)
    nombre_t = CharField(max_length=100, unique=True)
    apellido_p = CharField(max_length=100)
    apellido_m = CharField(max_length=100)
    puesto = CharField(max_length=100)
    fecha_nacimiento = DateField()
    curp = BooleanField()
    acta_nacimiento = BooleanField()
    ine = BooleanField()
    constancia_sf = BooleanField()
    constancia_ht = BooleanField()
    fotos = BooleanField()
    uniforme = BooleanField()
    correo = BooleanField()
    numero = BooleanField()
    contrasena = CharField(max_length=100)

    class Meta:
        database = database
        table_name = 'trabajador'


class Asistencia(Model):
    id = AutoField()
    user = ForeignKeyField(Trabajador, backref='asistencias')
    nombre_t = CharField(max_length=100)
    apellido_p = CharField(max_length=100)
    fecha = DateField()
    entrada = CharField(max_length=20)
    salida = CharField(max_length=20)
    retardo = CharField(max_length=20)
    descuento = CharField(max_length=20)
    mes = CharField(max_length=20)

    class Meta:
        database = database
        table_name = 'asistencias'


class Horario(Model):
    user = ForeignKeyField(Trabajador, primary_key=True)
    nombre_t = CharField(max_length=100)
    lunes = CharField(max_length=20)
    martes = CharField(max_length=20)
    miercoles = CharField(max_length=20)
    jueves = CharField(max_length=20)
    viernes = CharField(max_length=20)
    sabado = CharField(max_length=20)
    domingo = CharField(max_length=20)

    class Meta:
        database = database
        table_name = 'horario'


class Pago(Model):
    id = AutoField()
    user = ForeignKeyField(Trabajador, backref='pagos')
    nombre_t = CharField(max_length=100)
    puesto = CharField(max_length=100)
    pago = CharField(max_length=50)
    mes = CharField(max_length=20)
    pagado = BooleanField()

    class Meta:
        database = database
        table_name = 'pagos'


class Tarea(Model):
    id = AutoField()
    user = ForeignKeyField(Trabajador, backref='tareas')
    nombre_t = CharField(max_length=100)
    puesto = CharField(max_length=100)
    tarea = TextField()
    realizado = BooleanField()
    turno = CharField(max_length=50)

    class Meta:
        database = database
        table_name = 'tareas'


class Almacen(Model):
    producto_id = AutoField(primary_key=True)
    nombre_a = CharField(max_length=100)
    unidades = FloatField()
    tipo = CharField(max_length=50)
    responsable = CharField(max_length=100)
    user = ForeignKeyField(Trabajador, backref='almacen')

    class Meta:
        database = database
        table_name = 'almacen'


class Gasto(Model):
    gasto_id = AutoField(primary_key=True)
    producto = ForeignKeyField(Almacen, backref='gastos')
    nombre_a = CharField(max_length=100)
    unidades = IntegerField()
    costo = FloatField()
    fecha = CharField(max_length=20)
    tipo = CharField(max_length=50)
    responsable = CharField(max_length=100)
    user = ForeignKeyField(Trabajador, backref='gastos')

    class Meta:
        database = database
        table_name = 'gastos'


class Menu(Model):
    producto = ForeignKeyField(Almacen, primary_key=True)
    nombre_m = CharField(max_length=100)
    precio = CharField(max_length=20)
    descripcion = TextField()
    tortilla_maiz = IntegerField()
    tortilla_harina = IntegerField()
    cemita = IntegerField()
    aguacate = IntegerField()
    carne_res = IntegerField()
    carne_puerco = IntegerField()
    longaniza = IntegerField()
    cecina = IntegerField()
    chorizo_argentino = IntegerField()
    chicharron = IntegerField()
    salsa_quemada = IntegerField()
    chimichurri = IntegerField()
    cacahuate = IntegerField()
    papas = IntegerField()
    mayonesa = IntegerField()
    pico_gallo = IntegerField()
    crema_acida = IntegerField()
    rajas_crema = IntegerField()

    class Meta:
        database = database
        table_name = 'menu'


class Venta(Model):
    venta_id = AutoField(primary_key=True)
    producto = ForeignKeyField(Menu, backref='ventas')
    nombre_m = CharField(max_length=100)
    precio = CharField(max_length=20)
    cliente = ForeignKeyField(Cliente, backref='ventas')

    class Meta:
        database = database
        table_name = 'ventas'
