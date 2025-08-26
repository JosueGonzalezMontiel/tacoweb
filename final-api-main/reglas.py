#  Reglas y posibles hechos
base_conocimientos = [
    {
        'condiciones': ['estado_contento'],
        'conclusion': 'recomendar_electronica'
    },
    {
        'condiciones': ['estado_enojado'],
        'conclusion': 'recomendar_banda'
    },
    {
        'condiciones': ['estado_nostalgico'],
        'conclusion': 'recomendar_jose_jose'
    }
]

hechos_conocidos = set()

print("--- Sistema de Recomendación Musical por Estado de Ánimo (SBC) ---")


estado_animo = input("¿Cómo te sientes? (contento/enojado/nostalgico): ").lower()

if estado_animo == 'contento':
    hechos_conocidos.add('estado_contento')
elif estado_animo == 'enojado':
    hechos_conocidos.add('estado_enojado')
elif estado_animo == 'nostalgico':
    hechos_conocidos.add('estado_nostalgico')
else:
    print("Estado de ánimo no reconocido. No se puede hacer una recomendación.")

print(f"\nHechos conocidos: {hechos_conocidos}")

# Inferencia
conclusiones_inferidas = set()
cambios_hechos = True

while cambios_hechos:
    cambios_hechos = False
    for regla in base_conocimientos:
        todas_condiciones_cumplidas = all(cond in hechos_conocidos for cond in regla['condiciones'])

        if todas_condiciones_cumplidas and regla['conclusion'] not in conclusiones_inferidas:
            conclusiones_inferidas.add(regla['conclusion'])
            hechos_conocidos.add(regla['conclusion'])
            cambios_hechos = True
            print(f"  Regla disparada: '{regla['conclusion']}'")


print("\n--- Recomendación Final ---")
if 'recomendar_electronica' in conclusiones_inferidas:
    print("🎧 Te recomiendo escuchar música electrónica para mantener tu buen ánimo.")
elif 'recomendar_banda' in conclusiones_inferidas:
    print("🎺 Te recomiendo escuchar música de banda para liberar esa energía.")
elif 'recomendar_jose_jose' in conclusiones_inferidas:
    print("🎤 Te recomiendo escuchar a José José para acompañar tu nostalgia.")
else:
    print("No tengo una recomendación musical con el conocimiento actual.")

print("\nConclusiones inferidas por el sistema:", conclusiones_inferidas)