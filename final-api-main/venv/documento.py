import json
from docx import Document

# Leer el JSON de entrada
json_data = '''
{
    "id_factura": 3,
    "referencia_id": 2,
    "auto": "Jetta",
    "modelo": 2006,
    "version": "Bicentenario",
    "color": "Azul Metálico",
    "precio": 50000,
    "transmision": "Estándar",
    "motor": "2.0 lts 115cv",
    "n_motor": 343434,
    "n_puertas": 4,
    "tipo": "9CPLP",
    "chasis": "XXXX-AXXXCVV-XXX",
    "fecha_aprovacion": 20020306,
    "certificado": 2147483647,
    "id_cliente_id": 2,
    "nombre": "Josue",
    "numero": "222744553",
    "Direccion": "dfwe",
    "Colonia": "efw",
    "Estado": "efew",
    "CP": 23333,
    "Pais": "fwer",
    "numero_pagos": 23,
    "orden_envio": 1234,
    "fecha": "2024-06-21",
    "hora": "10:00"
}
'''

data = json.loads(json_data)

# Cargar el documento de plantilla
template_path = r"C:\Users\gonsa\Downloads\plantilla_factura.docx"
doc = Document(template_path)

# Función para reemplazar texto en el documento
def replace_text(doc, placeholder, replacement):
    for paragraph in doc.paragraphs:
        if placeholder in paragraph.text:
            paragraph.text = paragraph.text.replace(placeholder, str(replacement))
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                if placeholder in cell.text:
                    cell.text = cell.text.replace(placeholder, str(replacement))

# Reemplazar los marcadores de posición con los valores del JSON
replace_text(doc, "{{id_factura}}", data["id_factura"])
replace_text(doc, "{{referencia_id}}", data["referencia_id"])
replace_text(doc, "{{auto}}", data["auto"])
replace_text(doc, "{{modelo}}", data["modelo"])
replace_text(doc, "{{version}}", data["version"])
replace_text(doc, "{{color}}", data["color"])
replace_text(doc, "{{precio}}", data["precio"])
replace_text(doc, "{{transmision}}", data["transmision"])
replace_text(doc, "{{motor}}", data["motor"])
replace_text(doc, "{{n_motor}}", data["n_motor"])
replace_text(doc, "{{n_puertas}}", data["n_puertas"])
replace_text(doc, "{{tipo}}", data["tipo"])
replace_text(doc, "{{chasis}}", data["chasis"])
replace_text(doc, "{{fecha_aprovacion}}", data["fecha_aprovacion"])
replace_text(doc, "{{certificado}}", data["certificado"])
replace_text(doc, "{{id_cliente_id}}", data["id_cliente_id"])
replace_text(doc, "{{nombre}}", data["nombre"])
replace_text(doc, "{{numero}}", data["numero"])
replace_text(doc, "{{Direccion}}", data["Direccion"])
replace_text(doc, "{{Colonia}}", data["Colonia"])
replace_text(doc, "{{Estado}}", data["Estado"])
replace_text(doc, "{{CP}}", data["CP"])
replace_text(doc, "{{Pais}}", data["Pais"])
replace_text(doc, "{{numero_pagos}}", data["numero_pagos"])
replace_text(doc, "{{orden_envio}}", data["orden_envio"])
replace_text(doc, "{{fecha}}", data["fecha"])
replace_text(doc, "{{hora}}", data["hora"])

# Guardar el documento generado
output_path = r"C:\Users\gonsa\Downloads\factura_generada.docx"
doc.save(output_path)

print(f"Documento generado y guardado en: {output_path}")
