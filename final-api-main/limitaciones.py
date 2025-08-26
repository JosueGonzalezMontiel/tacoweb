from pydantic import BaseModel, Field
from typing import Optional


# Cliente
class ClienteRequestModel(BaseModel):
    nombre: str
    numero: int
    contrasena: str

    class Config:
        orm_mode = True
        from_attributes = True


class ClienteResponseModel(ClienteRequestModel):
    cliente_id: int


# Administrador
class AdministradorRequestModel(BaseModel):
    nombre: str
    contrasena: str

    class Config:
        orm_mode = True
        from_attributes = True


class AdministradorResponseModel(AdministradorRequestModel):
    admin_id: int


# Trabajador
class TrabajadorRequestModel(BaseModel):
    nombre_t: str
    apellido_p: str
    apellido_m: str
    puesto: str
    fecha_nacimiento: Optional[str] = None
    curp: bool
    acta_nacimiento: bool
    ine: bool
    constancia_sf: bool
    constancia_ht: bool
    fotos: bool
    uniforme: bool
    correo: bool
    numero: bool
    contrasena: str

    class Config:
        orm_mode = True
        from_attributes = True


class TrabajadorResponseModel(TrabajadorRequestModel):
    user_id: int


# Asistencias
class AsistenciaRequestModel(BaseModel):
    user_id: int
    nombre_t: str
    apellido_p: str
    fecha: Optional[str] = None
    entrada: str
    salida: str
    retardo: str
    descuento: str
    mes: str

    class Config:
        from_attributes = True


class AsistenciaResponseModel(AsistenciaRequestModel):
    id: int


# Horario
class HorarioRequestModel(BaseModel):
    user: int
    nombre_t: str
    lunes: Optional[str] = None
    martes: Optional[str] = None
    miercoles: Optional[str] = None
    jueves: Optional[str] = None
    viernes: Optional[str] = None
    sabado: Optional[str] = None
    domingo: Optional[str] = None

    class Config:
        
        from_attributes = True


class HorarioResponseModel(HorarioRequestModel):
    class Config:
        from_attributes = True


# Pagos
class PagoRequestModel(BaseModel):
    user_id: int
    nombre_t: str
    puesto: str
    pago: str
    mes: str
    pagado: bool

    class Config:
        orm_mode = True
        from_attributes = True


class PagoResponseModel(PagoRequestModel):
    id: int


# Tareas
class TareaRequestModel(BaseModel):
    user_id: int
    nombre_t: str
    puesto: str
    tarea: str
    realizado: bool
    turno: str

    class Config:
        orm_mode = True
        from_attributes = True


class TareaResponseModel(TareaRequestModel):
    id: int


# Almacén
class AlmacenRequestModel(BaseModel):
    nombre_a: str
    unidades: float
    tipo: str
    responsable: str
    user_id: int

    class Config:
        orm_mode = True
        from_attributes = True


class AlmacenResponseModel(AlmacenRequestModel):
    producto_id: int


# Gastos
class GastoRequestModel(BaseModel):
    producto_id: int
    nombre_a: str
    unidades: int
    costo: float
    fecha: str
    tipo: str
    responsable: str
    user_id: int

    class Config:
        orm_mode = True
        from_attributes = True


class GastoResponseModel(GastoRequestModel):
    gasto_id: int


# Menú
class MenuRequestModel(BaseModel):
    producto_id: int
    nombre_m: str
    precio: str
    descripcion: str
    tortilla_maiz: int
    tortilla_harina: int
    cemita: int
    aguacate: int
    carne_res: int
    carne_puerco: int
    longaniza: int
    cecina: int
    chorizo_argentino: int
    chicharron: int
    salsa_quemada: int
    chimichurri: int
    cacahuate: int
    papas: int
    mayonesa: int
    pico_gallo: int
    crema_acida: int
    rajas_crema: int

    class Config:
        orm_mode = True
        from_attributes = True


class MenuResponseModel(MenuRequestModel):
    pass  # Mismo contenido


# Ventas
class VentaRequestModel(BaseModel):
    producto_id: int
    nombre_m: str
    precio: str
    cliente_id: int

    class Config:
        orm_mode = True
        from_attributes = True


class VentaResponseModel(VentaRequestModel):
    venta_id: int
