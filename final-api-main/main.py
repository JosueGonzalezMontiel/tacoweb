from fastapi import FastAPI, Body, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from conexion import database as connection
from modelos import *
from limitaciones import *
from typing import List
import os
from openai import OpenAI
import httpx
import json
import re
from peewee import RawQuery
import pymysql
import matplotlib.pyplot as plt
import io
import base64




client = OpenAI(
    api_key="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",
    base_url="https://openrouter.ai/api/v1"
)

app = FastAPI(
    title='api ccc',
    description='api para maneacion de archivos',
    version='1.1'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event('startup')
async def startup_event():
    if connection.is_closed():
        connection.connect()
        connection.create_tables([
            Cliente,
            Administrador,
            Trabajador,
            Asistencia,
            Horario,
            Pago,
            Tarea,
            Almacen,
            Gasto,
            Menu,
            Venta
        ])

@app.on_event('shutdown')
def shutdown_event():
    if not connection.is_closed():
        connection.close()

@app.get('/')
async def index():
    return 'hola dfrr'

def trabajador():
    @app.post('/trabajador', response_model=TrabajadorResponseModel)
    async def create_trabajador(trabajador_data: TrabajadorRequestModel):
        nuevo = Trabajador.create(
            nombre_t=trabajador_data.nombre_t,
            apellido_p=trabajador_data.apellido_p,
            apellido_m=trabajador_data.apellido_m,
            puesto=trabajador_data.puesto,
            fecha_nacimiento=trabajador_data.fecha_nacimiento,
            curp=trabajador_data.curp,
            acta_nacimiento=trabajador_data.acta_nacimiento,
            ine=trabajador_data.ine,
            constancia_sf=trabajador_data.constancia_sf,
            constancia_ht=trabajador_data.constancia_ht,
            fotos=trabajador_data.fotos,
            uniforme=trabajador_data.uniforme,
            correo=trabajador_data.correo,
            numero=trabajador_data.numero,
            contrasena=trabajador_data.contrasena
        )
        return TrabajadorResponseModel(**nuevo.__data__)


    @app.get('/trabajador/{user_id}', response_model=TrabajadorResponseModel)
    async def get_trabajador(user_id: int):
        t = Trabajador.get_or_none(Trabajador.user_id == user_id)
        if not t:
            raise HTTPException(status_code=404, detail="Trabajador no encontrado")
        return TrabajadorResponseModel(**t.__data__)


    @app.get('/trabajadores', response_model=List[TrabajadorResponseModel])
    async def get_all_trabajadores():
        lista = Trabajador.select()
        result = []
        for t in lista:
            data = t.__data__.copy()
            if isinstance(data.get("fecha_nacimiento"), (str, type(None))):
                pass
            else:
                data["fecha_nacimiento"] = str(data["fecha_nacimiento"])
            result.append(TrabajadorResponseModel(**data))
        return result


    @app.put('/trabajador/{user_id}', response_model=TrabajadorResponseModel)
    async def update_trabajador(user_id: int, data: TrabajadorRequestModel):
        t = Trabajador.get_or_none(Trabajador.user_id == user_id)
        if not t:
            raise HTTPException(status_code=404, detail="Trabajador no encontrado")

        t.nombre_t = data.nombre_t
        t.apellido_p = data.apellido_p
        t.apellido_m = data.apellido_m
        t.puesto = data.puesto
        t.fecha_nacimiento = data.fecha_nacimiento
        t.curp = data.curp
        t.acta_nacimiento = data.acta_nacimiento
        t.ine = data.ine
        t.constancia_sf = data.constancia_sf
        t.constancia_ht = data.constancia_ht
        t.fotos = data.fotos
        t.uniforme = data.uniforme
        t.correo = data.correo
        t.numero = data.numero
        t.contrasena = data.contrasena

        t.save()
        return TrabajadorResponseModel(**t.__data__)


    @app.delete('/trabajador/{user_id}')
    async def delete_trabajador(user_id: int):
        t = Trabajador.get_or_none(Trabajador.user_id == user_id)
        if not t:
            raise HTTPException(status_code=404, detail="Trabajador no encontrado")
        t.delete_instance()
        return {"message": "Trabajador eliminado correctamente"}

def asistencia():
    @app.post('/asistencia', response_model=AsistenciaRequestModel)
    async def create_asistencia(asistencia_data: AsistenciaRequestModel):
        nueva_asistencia = Asistencia.create(
            user=asistencia_data.user_id,
            nombre_t=asistencia_data.nombre_t,
            apellido_p=asistencia_data.apellido_p,
            fecha=asistencia_data.fecha,
            entrada=asistencia_data.entrada, 
            salida=asistencia_data.salida,
            retardo=asistencia_data.retardo,
            descuento=asistencia_data.descuento,
            mes=asistencia_data.mes
        )
        asistencia_dict = nueva_asistencia.__data__.copy()
        asistencia_dict['user_id'] = asistencia_dict.pop('user')
        return AsistenciaRequestModel(**asistencia_dict)
    
    
    @app.get('/asistencia/{id}', response_model=AsistenciaRequestModel)
    async def get_asistencia(id: int):
        asistencia = Asistencia.get_or_none(Asistencia.id == id)
        if not asistencia:
            raise HTTPException(status_code=404, detail="Asistencia no encontrada")
        asistencia_dict = asistencia.__data__.copy()
        asistencia_dict['user_id'] = asistencia_dict.pop('user')
        return AsistenciaRequestModel(**asistencia_dict)

    @app.get('/asistencias', response_model=List[AsistenciaRequestModel])
    async def get_all_asistencias():
        lista = Asistencia.select()
        result = []
        for a in lista:
            asistencia_dict = a.__data__.copy()
            asistencia_dict['user_id'] = asistencia_dict.pop('user')
            asistencia_dict['fecha'] = str(asistencia_dict['fecha'])
            result.append(AsistenciaRequestModel(**asistencia_dict))
        return result

    @app.put('/asistencia/{id}', response_model=AsistenciaRequestModel)
    async def update_asistencia(id: int, data: AsistenciaRequestModel):
        asistencia = Asistencia.get_or_none(Asistencia.id == id)
        if not asistencia:
            raise HTTPException(status_code=404, detail="Asistencia no encontrada")

        asistencia.user = data.user_id
        asistencia.nombre_t = data.nombre_t
        asistencia.apellido_p = data.apellido_p
        asistencia.fecha = data.fecha
        asistencia.entrada = data.entrada
        asistencia.salida = data.salida
        asistencia.retardo = data.retardo
        asistencia.descuento = data.descuento
        asistencia.mes = data.mes

        asistencia.save()
        asistencia_dict = asistencia.__data__.copy()
        asistencia_dict['user_id'] = asistencia_dict.pop('user')
        return AsistenciaRequestModel(**asistencia_dict)

    @app.delete('/asistencia/{id}')
    async def delete_asistencia(id: int):
        asistencia = Asistencia.get_or_none(Asistencia.id == id)
        if not asistencia:
            raise HTTPException(status_code=404, detail="Asistencia no encontrada")
        asistencia.delete_instance()
        return {"message": "Asistencia eliminada correctamente"}
    



def horario():
    @app.post('/horario', response_model=HorarioResponseModel)
    async def create_horario(horario_data: HorarioRequestModel):
        nuevo_horario = Horario.create(**horario_data.dict())
        horario_dict = nuevo_horario.__data__.copy()
        horario_dict['user'] = nuevo_horario.user.user_id  # Usa .user_id aquí
        return HorarioResponseModel(**horario_dict)

    @app.get('/horario/{user_id}', response_model=HorarioResponseModel)
    async def get_horario(user_id: int):
        horario = Horario.get_or_none(Horario.user == user_id)
        if not horario:
            raise HTTPException(status_code=404, detail="Horario no encontrado")
        horario_dict = horario.__data__.copy()
        horario_dict['user'] = horario.user.user_id
        return HorarioResponseModel(**horario_dict)

    @app.get('/horarios', response_model=List[HorarioResponseModel])
    async def get_all_horarios():
        lista = Horario.select()
        result = []
        for h in lista:
            horario_dict = h.__data__.copy()
            horario_dict['user'] = h.user.user_id
            result.append(HorarioResponseModel(**horario_dict))
        return result

    @app.put('/horario/{user_id}', response_model=HorarioResponseModel)
    async def update_horario(user_id: int, data: HorarioRequestModel):
        horario = Horario.get_or_none(Horario.user == user_id)
        if not horario:
            raise HTTPException(status_code=404, detail="Horario no encontrado")
        for key, value in data.dict().items():
            setattr(horario, key, value)
        horario.save()
        horario_dict = horario.__data__.copy()
        horario_dict['user'] = horario.user.user_id  # Corrige aquí
        return HorarioResponseModel(**horario_dict)

    @app.delete('/horario/{user_id}')
    async def delete_horario(user_id: int):
        horario = Horario.get_or_none(Horario.user == user_id)
        if not horario:
            raise HTTPException(status_code=404, detail="Horario no encontrado")
        horario.delete_instance()
        return {"message": "Horario eliminado correctamente"}   


def pago():
    @app.post('/pago', response_model=PagoResponseModel)
    async def create_pago(pago_data: PagoRequestModel):
        nuevo_pago = Pago.create(
            user=pago_data.user_id,
            nombre_t=pago_data.nombre_t,
            puesto=pago_data.puesto,
            pago=pago_data.pago,
            mes=pago_data.mes,
            pagado=pago_data.pagado
        )
        pago_dict = nuevo_pago.__data__.copy()
        pago_dict['user_id'] = pago_dict.pop('user')
        return PagoResponseModel(**pago_dict)


    @app.get('/pago/{id}', response_model=PagoResponseModel)
    async def get_pago(id: int):
        pago = Pago.get_or_none(Pago.id == id)
        if not pago:
            raise HTTPException(status_code=404, detail="Pago no encontrado")
        pago_dict = pago.__data__.copy()
        pago_dict['user_id'] = pago_dict.pop('user')
        return PagoResponseModel(**pago_dict)


    @app.get('/pagos', response_model=List[PagoResponseModel])
    async def get_all_pagos():
        lista = Pago.select()
        result = []
        for p in lista:
            pago_dict = p.__data__.copy()
            pago_dict['user_id'] = pago_dict.pop('user')
            result.append(PagoResponseModel(**pago_dict))
        return result


    @app.put('/pago/{id}', response_model=PagoResponseModel)
    async def update_pago(id: int, data: PagoRequestModel):
        pago = Pago.get_or_none(Pago.id == id)
        if not pago:
            raise HTTPException(status_code=404, detail="Pago no encontrado")

        pago.user = data.user_id
        pago.nombre_t = data.nombre_t
        pago.puesto = data.puesto
        pago.pago = data.pago
        pago.mes = data.mes
        pago.pagado = data.pagado

        pago.save()
        pago_dict = pago.__data__.copy()
        pago_dict['user_id'] = pago_dict.pop('user')
        return PagoResponseModel(**pago_dict)


    @app.delete('/pago/{id}')
    async def delete_pago(id: int):
        pago = Pago.get_or_none(Pago.id == id)
        if not pago:
            raise HTTPException(status_code=404, detail="Pago no encontrado")
        pago.delete_instance()
        return {"message": "Pago eliminado correctamente"}

def tarea():
    @app.post('/tarea', response_model=TareaResponseModel)
    async def create_tarea(tarea_data: TareaRequestModel):
        nueva_tarea = Tarea.create(
            user=tarea_data.user_id,
            nombre_t=tarea_data.nombre_t,
            puesto=tarea_data.puesto,
            tarea=tarea_data.tarea,
            realizado=tarea_data.realizado,
            turno=tarea_data.turno
        )
        tarea_dict = nueva_tarea.__data__.copy()
        tarea_dict['user_id'] = tarea_dict.pop('user')
        return TareaResponseModel(**tarea_dict)


    @app.get('/tarea/{id}', response_model=TareaResponseModel)
    async def get_tarea(id: int):
        tarea = Tarea.get_or_none(Tarea.id == id)
        if not tarea:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        tarea_dict = tarea.__data__.copy()
        tarea_dict['user_id'] = tarea_dict.pop('user')
        return TareaResponseModel(**tarea_dict)


    @app.get('/tareas', response_model=List[TareaResponseModel])
    async def get_all_tareas():
        lista = Tarea.select()
        result = []
        for t in lista:
            tarea_dict = t.__data__.copy()
            tarea_dict['user_id'] = tarea_dict.pop('user')
            result.append(TareaResponseModel(**tarea_dict))
        return result


    @app.put('/tarea/{id}', response_model=TareaResponseModel)
    async def update_tarea(id: int, data: TareaRequestModel):
        tarea = Tarea.get_or_none(Tarea.id == id)
        if not tarea:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")

        tarea.user = data.user_id
        tarea.nombre_t = data.nombre_t
        tarea.puesto = data.puesto
        tarea.tarea = data.tarea
        tarea.realizado = data.realizado
        tarea.turno = data.turno

        tarea.save()
        tarea_dict = tarea.__data__.copy()
        tarea_dict['user_id'] = tarea_dict.pop('user')
        return TareaResponseModel(**tarea_dict)


    @app.delete('/tarea/{id}')
    async def delete_tarea(id: int):
        tarea = Tarea.get_or_none(Tarea.id ==id)
        if not tarea:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        tarea.delete_instance()
        return {"message": "Tarea eliminada correctamente"}


def almacen():
    @app.post('/almacen', response_model=AlmacenResponseModel)
    async def create_almacen(almacen_data: AlmacenRequestModel):
        nuevo_almacen = Almacen.create(
            nombre_a=almacen_data.nombre_a,
            unidades=almacen_data.unidades,
            tipo=almacen_data.tipo,
            responsable=almacen_data.responsable,
            user=almacen_data.user_id
        )
        almacen_dict = nuevo_almacen.__data__.copy()
        almacen_dict['user_id'] = almacen_dict.pop('user')
        return AlmacenResponseModel(**almacen_dict)


    @app.get('/almacen/{producto_id}', response_model=AlmacenResponseModel)
    async def get_almacen(producto_id: int):
        almacen = Almacen.get_or_none(Almacen.producto_id == producto_id)
        if not almacen:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        almacen_dict = almacen.__data__.copy()
        almacen_dict['user_id'] = almacen_dict.pop('user')
        return AlmacenResponseModel(**almacen_dict)


    @app.get('/almacenes', response_model=List[AlmacenResponseModel])
    async def get_all_almacenes():
        lista = Almacen.select()
        result = []
        for a in lista:
            almacen_dict = a.__data__.copy()
            almacen_dict['user_id'] = almacen_dict.pop('user')
            result.append(AlmacenResponseModel(**almacen_dict))
        return result


    @app.put('/almacen/{producto_id}', response_model=AlmacenResponseModel)
    async def update_almacen(producto_id: int, data: AlmacenRequestModel):
        almacen = Almacen.get_or_none(Almacen.producto_id == producto_id)
        if not almacen:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

        for key, value in data.dict().items():
            setattr(almacen, key, value)

        almacen.save()
        almacen_dict = almacen.__data__.copy()
        almacen_dict['user_id'] = almacen_dict.pop('user')
        return AlmacenResponseModel(**almacen_dict)


    @app.delete('/almacen/{producto_id}')
    async def delete_almacen(producto_id: int):
        almacen = Almacen.get_or_none(Almacen.producto_id == producto_id)
        if not almacen:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        almacen.delete_instance()
        return {"message": "Producto eliminado correctamente"}
    
def gasto():
    @app.post('/gasto', response_model=GastoResponseModel)
    async def create_gasto(gasto_data: GastoRequestModel):
        nuevo_gasto = Gasto.create(
            producto=gasto_data.producto_id,
            nombre_a=gasto_data.nombre_a,
            unidades=gasto_data.unidades,
            costo=gasto_data.costo,
            fecha=gasto_data.fecha,
            tipo=gasto_data.tipo,
            responsable=gasto_data.responsable,
            user=gasto_data.user_id
        )
        gasto_dict = nuevo_gasto.__data__.copy()
        gasto_dict['user_id'] = gasto_dict.pop('user')
        gasto_dict['producto_id'] = gasto_dict.pop('producto')
        return GastoResponseModel(**gasto_dict)

    @app.get('/gasto/{gasto_id}', response_model=GastoResponseModel)
    async def get_gasto(gasto_id: int):
        gasto = Gasto.get_or_none(Gasto.gasto_id == gasto_id)
        if not gasto:
            raise HTTPException(status_code=404, detail="Gasto no encontrado")
        gasto_dict = gasto.__data__.copy()
        gasto_dict['user_id'] = gasto_dict.pop('user')
        gasto_dict['producto_id'] = gasto_dict.pop('producto')
        return GastoResponseModel(**gasto_dict)

    @app.get('/gastos', response_model=List[GastoResponseModel])
    async def get_all_gastos():
        lista = Gasto.select()
        result = []
        for g in lista:
            gasto_dict = g.__data__.copy()
            gasto_dict['user_id'] = gasto_dict.pop('user')
            gasto_dict['producto_id'] = gasto_dict.pop('producto')
            result.append(GastoResponseModel(**gasto_dict))
        return result

    @app.put('/gasto/{gasto_id}', response_model=GastoResponseModel)
    async def update_gasto(gasto_id: int, data: GastoRequestModel):
        gasto = Gasto.get_or_none(Gasto.gasto_id == gasto_id)
        if not gasto:
            raise HTTPException(status_code=404, detail="Gasto no encontrado")
        for key, value in data.dict().items():
            setattr(gasto, key, value)
        gasto.save()
        gasto_dict = gasto.__data__.copy()
        gasto_dict['user_id'] = gasto_dict.pop('user')
        gasto_dict['producto_id'] = gasto_dict.pop('producto')
        return GastoResponseModel(**gasto_dict)

    @app.delete('/gasto/{gasto_id}')
    async def delete_gasto(gasto_id: int):
        gasto = Gasto.get_or_none(Gasto.gasto_id == gasto_id)
        if not gasto:
            raise HTTPException(status_code=404, detail="Gasto no encontrado")
        gasto.delete_instance()
        return {"message": "Gasto eliminado correctamente"} 
    
    
def menu():
    @app.get('/menu', response_model=List[MenuResponseModel])
    async def get_menu():
        lista = Menu.select()
        result = []
        for m in lista:
            menu_dict = m.__data__.copy()
            menu_dict['producto_id'] = menu_dict.pop('producto')
            result.append(MenuResponseModel(**menu_dict))
        return result

    @app.post('/menu', response_model=MenuResponseModel)
    async def create_menu(menu_data: MenuRequestModel):
        nuevo_menu = Menu.create(**menu_data.dict())
        menu_dict = nuevo_menu.__data__.copy()
        menu_dict['producto_id'] = menu_dict.pop('producto')
        return MenuResponseModel(**menu_dict)

    @app.delete('/menu/{id}')
    async def delete_menu(id: int):
        menu = Menu.get_or_none(Menu.producto == id)
        if not menu:
            raise HTTPException(status_code=404, detail="Menu no encontrado")
        menu.delete_instance()
        return {"message": "Menu eliminado correctamente"}
    @app.put('/menu/{id}', response_model=MenuResponseModel)
    async def update_menu(id: int, data: MenuRequestModel):
        menu = Menu.get_or_none(Menu.producto == id)
        if not menu:
            raise HTTPException(status_code=404, detail="Menu no encontrado")
        for key, value in data.dict().items():
            setattr(menu, key, value)
        menu.save()
        menu_dict = menu.__data__.copy()
        menu_dict['producto_id'] = menu_dict.pop('producto')
        return MenuResponseModel(**menu_dict)
    @app.get('/menu/{id}', response_model=MenuResponseModel)
    async def get_menu_by_id(id: int):
        menu = Menu.get_or_none(Menu.producto == id)
        if not menu:
            raise HTTPException(status_code=404, detail="Menu no encontrado")
        menu_dict = menu.__data__.copy()
        menu_dict['producto_id'] = menu_dict.pop('producto')
        return MenuResponseModel(**menu_dict)

def cliente():
    @app.post('/cliente', response_model=ClienteResponseModel)
    async def create_cliente(cliente_data: ClienteRequestModel):
        nuevo_cliente = Cliente.create(**cliente_data.dict())
        return ClienteResponseModel(**nuevo_cliente.__data__)

    @app.get('/cliente/{id}', response_model=ClienteResponseModel)
    async def get_cliente(id: int):
        cliente = Cliente.get_or_none(Cliente.cliente_id == id)
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        return ClienteResponseModel(**cliente.__data__)

    @app.get('/clientes', response_model=List[ClienteResponseModel])
    async def get_all_clientes():
        lista = Cliente.select()
        return [ClienteResponseModel(**c.__data__) for c in lista]

    @app.put('/cliente/{id}', response_model=ClienteResponseModel)
    async def update_cliente(id: int, data: ClienteRequestModel):
        cliente = Cliente.get_or_none(Cliente.cliente_id == id)
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        for key, value in data.dict().items():
            setattr(cliente, key, value)
        cliente.save()
        return ClienteResponseModel(**cliente.__data__)

    @app.delete('/cliente/{id}')
    async def delete_cliente(id: int):
        cliente = Cliente.get_or_none(Cliente.cliente_id == id)
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        cliente.delete_instance()
        return {"message": "Cliente eliminado correctamente"}
    
def administrador():
    @app.post('/administrador', response_model=AdministradorResponseModel)
    async def create_administrador(admin_data: AdministradorRequestModel):
        nuevo_admin = Administrador.create(**admin_data.dict())
        return AdministradorResponseModel(**nuevo_admin.__data__)

    @app.get('/administrador/{id}', response_model=AdministradorResponseModel)
    async def get_administrador(id: int):
        admin = Administrador.get_or_none(Administrador.admin_id == id)
        if not admin:
            raise HTTPException(status_code=404, detail="Administrador no encontrado")
        return AdministradorResponseModel(**admin.__data__)

    @app.get('/administradores', response_model=List[AdministradorResponseModel])
    async def get_all_administradores():
        lista = Administrador.select()
        return [AdministradorResponseModel(**a.__data__) for a in lista]

    @app.put('/administrador/{id}', response_model=AdministradorResponseModel)
    async def update_administrador(id: int, data: AdministradorRequestModel):
        admin = Administrador.get_or_none(Administrador.admin_id == id)
        if not admin:
            raise HTTPException(status_code=404, detail="Administrador no encontrado")
        for key, value in data.dict().items():
            setattr(admin, key, value)
        admin.save()
        return AdministradorResponseModel(**admin.__data__)

    @app.delete('/administrador/{id}')
    async def delete_administrador(id: int):
        admin = Administrador.get_or_none(Administrador.admin_id == id)
        if not admin:
            raise HTTPException(status_code=404, detail="Administrador no encontrado")
        admin.delete_instance()
        return {"message": "Administrador eliminado correctamente"}
    

def venta():
    @app.post('/venta', response_model=VentaResponseModel)
    async def create_venta(venta_data: VentaRequestModel):
        nueva_venta = Venta.create(**venta_data.dict())
        return VentaResponseModel(**nueva_venta.__data__)

    @app.get('/venta/{id}', response_model=VentaResponseModel)
    async def get_venta(id: int):
        venta = Venta.get_or_none(Venta.venta_id == id)
        if not venta:
            raise HTTPException(status_code=404, detail="Venta no encontrada")
        return VentaResponseModel(**venta.__data__)

    @app.get('/ventas', response_model=List[VentaResponseModel])
    async def get_all_ventas():
        lista = Venta.select()
        return [VentaResponseModel(**v.__data__) for v in lista]

    @app.put('/venta/{id}', response_model=VentaResponseModel)
    async def update_venta(id: int, data: VentaRequestModel):
        venta = Venta.get_or_none(Venta.venta_id == id)
        if not venta:
            raise HTTPException(status_code=404, detail="Venta no encontrada")
        for key, value in data.dict().items():
            setattr(venta, key, value)
        venta.save()
        return VentaResponseModel(**venta.__data__)

    @app.delete('/venta/{id}')
    async def delete_venta(id: int):
        venta = Venta.get_or_none(Venta.venta_id == id)
        if not venta:
            raise HTTPException(status_code=404, detail="Venta no encontrada")
        venta.delete_instance()
        return {"message": "Venta eliminado correctamente"}
    

trabajador()
asistencia()
horario()
administrador()
gasto()
menu()
cliente()
venta()
almacen()
tarea()
pago()


conversaciones = {}

def es_peticion_grafica(historial):
    
    for h in reversed(historial):
        if h["role"] == "user" and "gráfica" in h["content"].lower():
            return True
    return False

def es_peticion_grafica_actual(message: str):
    return "gráfica" in message.lower() or "grafica" in message.lower()

@app.post("/chatbot")
async def chatbot(message: str = Body(..., embed=True), request: Request = None):
    user_id = request.client.host
    historial = conversaciones.get(user_id, [])
    historial.append({"role": "user", "content": message})

   
    if len(historial) == 1:
        menu = (
            "¡Hola! Soy tu asistente de base de datos para el restaurante.\n"
            "Puedes pedirme:\n"
            "1. Registrar, consultar, actualizar o eliminar clientes, trabajadores, asistencias, ventas, etc.\n"
            "2. Consultar datos específicos (ejemplo: 'Muéstrame las asistencias de Juan').\n"
            "3. Generar gráficas de datos (ejemplo: 'Genera una gráfica de barras de retardos por trabajador').\n"
            "4. Consultar pagos, horarios, menús, gastos y más.\n"
            "Por favor, dime qué deseas hacer."
        )
        conversaciones[user_id] = historial
        return {"response": menu}

    with open("esquema_bd.txt", "r", encoding="utf-8") as f:
        esquema = f.read()

    system_prompt = f"""
Eres un asistente experto en bases de datos MySQL para un restaurante.
Este es el esquema de la base de datos:
{esquema}

Cuando el usuario quiera agregar (INSERT) o actualizar (UPDATE) un registro y no proporcione todos los datos necesarios,
debes pedir los datos uno por uno, haciendo **solo una pregunta por mensaje** sobre el siguiente campo requerido, indicando el nombre, el tipo de dato y un ejemplo de entrada.
Cuando tengas todos los datos, genera la consulta SQL correspondiente y devuélvela (sin explicación ni formato markdown).

Si el usuario pide una gráfica, genera primero la consulta SQL necesaria para obtener los datos y responde solo con el SQL.

Si el usuario comete un error o no hay datos para mostrar, responde con un mensaje claro y amigable explicando el problema y cómo corregirlo.

Ejemplo de flujo:
Usuario: Quiero registrar un cliente nuevo.
Asistente: ¿Cuál es el nombre del cliente (tipo VARCHAR(100), ejemplo: Juan Pérez)?
Usuario: Juan Pérez
Asistente: ¿Cuál es el número del cliente (tipo BIGINT, ejemplo: 5551234567)?
Usuario: 5551234567
Asistente: ¿Cuál es la contraseña del cliente (tipo VARCHAR(100), ejemplo: juan2024)?
Usuario: juan2024
Asistente: INSERT INTO cliente (nombre, numero, contrasena) VALUES ('Juan Pérez', 5551234567, 'juan2024');

Recuerda: **Nunca preguntes más de un campo a la vez**.
"""

    messages = [{"role": "system", "content": system_prompt}] + historial

    response = client.chat.completions.create(
        model="deepseek/deepseek-r1:free",
        messages=messages
    )
    ai_reply = response.choices[0].message.content.strip()
    historial.append({"role": "assistant", "content": ai_reply})
    conversaciones[user_id] = historial

    sql_query = extraer_sql(ai_reply)
    resultado = None
    if ai_reply.lower().startswith(("select", "insert", "update", "delete")) or sql_query.lower().startswith(("select", "insert", "update", "delete")):
        resultado = ejecutar_sql(sql_query)

   
    if es_peticion_grafica_actual(message) and resultado and "result" in resultado:
        datos = resultado["result"]
        if not datos:
            return {"response": "No se encontraron datos para generar la gráfica. Por favor, verifica que existan registros con los criterios solicitados o intenta con otros parámetros."}
        img_base64, error = generar_grafica_barras(datos)
        if error:
            return {"response": error}
        return img_base64  

    if resultado is not None:
        return resultado
    else:
        return {"response": ai_reply}


def ejecutar_sql(query):
   
    query_lower = query.strip().lower()
    if not (
        query_lower.startswith("select")
        or query_lower.startswith("insert")
        or query_lower.startswith("update")
        or query_lower.startswith("delete")
    ):
        return {"error": "Solo se permiten SELECT, INSERT, UPDATE y DELETE.", "sql": query}

    if any(cmd in query_lower for cmd in ["drop ", "alter ", "truncate ", "create ", "replace "]):
        return {"error": "Comando SQL no permitido por seguridad.", "sql": query}
    try:
        conn = connection.connection()
        with conn.cursor() as cursor:
            cursor.execute(query)
            if query_lower.startswith("select"):
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                result = [dict(zip(columns, row)) for row in rows]
                return {"result": result, "sql": query}
            else:
                conn.commit()
                return {"message": "Operación realizada correctamente.", "sql": query}
    except Exception as e:
        return {"error": str(e), "sql": query}

def generar_grafica_barras(datos):
    if not datos or len(datos) == 0:
        return None, "No hay datos para graficar."
    columnas = list(datos[0].keys())
    col_texto = None
    col_num = None
    for col in columnas:
        if isinstance(datos[0][col], (int, float)):
            col_num = col
        elif isinstance(datos[0][col], str):
            col_texto = col
        if col_texto and col_num:
            break
    if not (col_texto and col_num):
        col_texto, col_num = columnas[0], columnas[1]
    x = [str(d[col_texto]) for d in datos]
    y = []
    for d in datos:
        try:
            y.append(float(d[col_num]))
        except Exception:
            y.append(0)
    plt.figure(figsize=(10, 6))
    plt.bar(x, y)
    plt.xlabel(col_texto)
    plt.ylabel(col_num)
    plt.title(f"Gráfica de barras: {col_texto} vs {col_num}")
    plt.xticks(rotation=90)  
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    return img_base64, None

def extraer_sql(texto):
    match = re.search(r'```sql\s*(.*?)\s*```', texto, re.DOTALL)
    if match:
        return match.group(1).strip()
    return texto.strip()





