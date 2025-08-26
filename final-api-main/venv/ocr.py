import pytesseract as tess
from PIL import Image
import cv2
import json
import re

# Configuración del comando de Tesseract
tess.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Cargar la imagen y convertir a escala de grises
image_path = r'C:\\Users\\gonsa\\Desktop\\backend2-main\\venv\\inesreal.jpg'
ine = cv2.imread(image_path)
gray = cv2.cvtColor(ine, cv2.COLOR_BGR2GRAY)

# Aplicar umbralización para mejorar el contraste del texto
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

# Convertir la imagen a texto
txt = tess.image_to_string(ine) 
print("Texto OCR:")
print(txt)

# Función para limpiar y extraer datos
def extract_data(text):
    data = {}
    # Intenta extraer cada campo usando expresiones regulares más detalladas
    nombre_match = re.search(r'(?<=NOMBRE\s)[\s\S]*?(?=DOMICILIO)', text)
    if nombre_match:
        # Reemplazar saltos de línea con espacios para el nombre
        data['nombre'] = re.sub(r'\s+', ' ', nombre_match.group().strip())

    # Extraer dirección y colonia usando un patrón robusto que maneja mejor los saltos de línea
    domicilio_pattern = re.compile(r'DOMICILIO\.\s*([\s\S]*?)COL\.\s*([\s\S]*?)C\.P\.\s*(\d+)')
    domicilio_match = domicilio_pattern.search(text)
    if domicilio_match:
        data['direccion'] = domicilio_match.group(1).strip()
        # Reemplazar saltos de línea con espacios para la colonia
        data['colonia'] = re.sub(r'\s+', ' ', domicilio_match.group(2).strip())
        data['cp'] = int(domicilio_match.group(3).strip())

    # Extraer estado
    estado_match = re.search(r'C\.P\.\s+\d+,\s+([\s\S]*?)(?=,|\n)', text)
    if estado_match:
        data['estado'] = re.sub(r'\s+', ' ', estado_match.group(1).strip())

    # Asumir que el país es México
    data['pais'] = 'México'
    
    return data

# Extraer datos
data = extract_data(txt)

# Convertir datos a JSON
json_data = json.dumps(data, ensure_ascii=False, indent=4)

# Imprimir el texto extraído y los datos en formato JSON
print("\nDatos en JSON:")
print(json_data)

# Mostrar la imagen
cv2.imshow('imagen', ine)
cv2.waitKey(0)
cv2.destroyAllWindows()
