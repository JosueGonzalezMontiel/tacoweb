
base_conocimientos = [
    {
        'condiciones': ['con_familia'],
        'conclusion': 'recomendar_comedia_familiar'
    },
    {
        'condiciones': ['con_novia'],
        'conclusion': 'recomendar_pelicula_romantica'
    },
    {
        'condiciones': ['con_amigos'],
        'conclusion': 'recomendar_comedia_picante'
    }
]

hechos_conocidos = set()

print("--- Sistema de Recomendación de Películas según Compañía (SBC) ---")


companero = input("¿Con quién estás? (familia/novia/amigos): ").lower()

if companero == 'familia':
    hechos_conocidos.add('con_familia')
elif companero == 'novia':
    hechos_conocidos.add('con_novia')
elif companero == 'amigos':
    hechos_conocidos.add('con_amigos')
else:
    print("No reconozco con quién estás. No puedo hacer una recomendación.")

print(f"\nHechos conocidos: {hechos_conocidos}")


conclusiones_inferidas = set()
cambios_hechos = True

while cambios_hechos:
    cambios_hechos = False
    for regla in base_conocimientos:
        todas_condiciones_cumplidas = all(
            (cond in hechos_conocidos if not cond.startswith('no_') else cond[3:] not in hechos_conocidos)
            for cond in regla['condiciones']
        )

        if todas_condiciones_cumplidas and regla['conclusion'] not in conclusiones_inferidas:
            conclusiones_inferidas.add(regla['conclusion'])
            hechos_conocidos.add(regla['conclusion'])
            cambios_hechos = True
            print(f"  Regla disparada: '{regla['conclusion']}'")


print("\n--- Recomendación Final ---")
if 'recomendar_comedia_familiar' in conclusiones_inferidas:
    print(" Te recomiendo una comedia familiar para disfrutar con tus seres queridos.")
elif 'recomendar_pelicula_romantica' in conclusiones_inferidas:
    print(" Te recomiendo una película romántica para compartir con tu pareja.")
elif 'recomendar_comedia_picante' in conclusiones_inferidas:
    print(" Te recomiendo una comedia picante para reírte con tus amigos.")
else:
    print("No tengo una recomendación específica con el conocimiento actual.")

print("\nConclusiones inferidas por el sistema:", conclusiones_inferidas)
