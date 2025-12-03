"""
Interfaz interactiva para el Agente de Aprendizaje de Estudiantes de TI.

Esta interfaz permite a los estudiantes interactuar con el agente de manera
sencilla a través de línea de comandos.
"""

from agente import AgenteEstudianteTI


def mostrar_menu_principal():
    """Muestra el menú principal del agente."""
    print("\n" + "=" * 50)
    print("🎓 AGENTE DE APRENDIZAJE PARA ESTUDIANTES DE TI")
    print("=" * 50)
    print("\n¿Qué deseas hacer?\n")
    print("1. 📋 Ver rutas de aprendizaje predefinidas")
    print("2. 🎯 Crear una ruta de aprendizaje personalizada")
    print("3. 🔍 Buscar cursos por habilidad")
    print("4. 📚 Ver todos los cursos por categoría")
    print("5. ❓ Resolver una duda sobre un tema")
    print("6. ℹ️  Información del agente")
    print("7. 🚪 Salir")
    print()


def ver_rutas_predefinidas(agente: AgenteEstudianteTI):
    """Muestra las rutas de aprendizaje predefinidas."""
    rutas = agente.listar_rutas_predefinidas()
    
    print("\n📌 RUTAS DE APRENDIZAJE PREDEFINIDAS")
    print("-" * 40)
    
    for i, ruta in enumerate(rutas, 1):
        print(f"\n{i}. {ruta['nombre']}")
        print(f"   {ruta['descripcion']}")
        print(f"   ⏱️  Duración total: {ruta['duracion_total_horas']} horas")
    
    while True:
        opcion = input("\n¿Deseas ver los detalles de alguna ruta? (número o 'n' para volver): ")
        if opcion.lower() == 'n':
            break
        
        try:
            idx = int(opcion) - 1
            if 0 <= idx < len(rutas):
                ruta_id = list(agente.rutas_predefinidas.keys())[idx]
                ruta_detalle = agente.obtener_ruta_predefinida(ruta_id)
                mostrar_detalle_ruta(ruta_detalle)
            else:
                print("❌ Opción no válida.")
        except ValueError:
            print("❌ Por favor ingresa un número válido.")


def mostrar_detalle_ruta(ruta: dict):
    """Muestra los detalles de una ruta de aprendizaje."""
    print(f"\n🎯 {ruta['nombre']}")
    print(f"📝 {ruta['descripcion']}")
    print(f"\n📚 Cursos incluidos:")
    
    for i, curso in enumerate(ruta['cursos'], 1):
        print(f"\n   {i}. {curso['nombre']}")
        print(f"      Nivel: {curso['nivel']} | Duración: {curso['duracion_horas']}h")
        print(f"      {curso['descripcion']}")
    
    print(f"\n⏱️  Duración total: {ruta['duracion_total_horas']} horas")


def crear_ruta_personalizada(agente: AgenteEstudianteTI):
    """Guía al usuario para crear una ruta de aprendizaje personalizada."""
    print("\n🎯 CREAR RUTA DE APRENDIZAJE PERSONALIZADA")
    print("-" * 40)
    
    # Obtener habilidades objetivo
    print("\n¿Qué habilidades deseas aprender?")
    print("Ejemplos: Python, JavaScript, SQL, Docker, AWS, React, etc.")
    habilidades_input = input("Ingresa las habilidades separadas por coma: ")
    habilidades = [h.strip() for h in habilidades_input.split(",") if h.strip()]
    
    if not habilidades:
        print("❌ No ingresaste ninguna habilidad.")
        return
    
    # Obtener horas disponibles
    print("\n¿Cuántas horas a la semana puedes dedicar al estudio?")
    try:
        horas = int(input("Horas por semana (ej: 5): "))
    except ValueError:
        horas = 5
        print("⚠️ Usando valor por defecto: 5 horas")
    
    # Obtener nivel actual
    print("\n¿Cuál es tu nivel actual en TI?")
    print("1. Principiante")
    print("2. Intermedio")
    print("3. Avanzado")
    
    nivel_opcion = input("Selecciona (1-3): ").strip()
    niveles = {"1": "principiante", "2": "intermedio", "3": "avanzado"}
    nivel = niveles.get(nivel_opcion, "principiante")
    
    # Generar ruta
    ruta = agente.generar_ruta_personalizada(habilidades, horas, nivel)
    
    print("\n" + "=" * 50)
    print("✅ ¡RUTA PERSONALIZADA GENERADA!")
    print("=" * 50)
    
    print(f"\n🎯 Habilidades objetivo: {', '.join(ruta['habilidades_objetivo'])}")
    print(f"📊 Tu nivel: {ruta['nivel_actual']}")
    print(f"⏰ Tiempo de estudio semanal: {ruta['horas_semanales']} horas")
    print(f"📅 Tiempo estimado para completar: {ruta['semanas_estimadas']} semanas")
    
    if ruta['cursos']:
        print("\n📚 Tu ruta de aprendizaje:")
        for i, curso in enumerate(ruta['cursos'], 1):
            print(f"\n   {i}. {curso['nombre']}")
            print(f"      Nivel: {curso['nivel']} | Duración: {curso['duracion_horas']}h")
            print(f"      Temas: {', '.join(curso['temas'][:3])}")
    else:
        print("\n⚠️ No encontré cursos que coincidan con esas habilidades.")
        print("   Intenta con: Python, JavaScript, SQL, Docker, Git, Linux, etc.")
    
    print("\n💡 Tips para optimizar tu estudio:")
    for tip in ruta['tips_estudiante_trabajador']:
        print(f"   {tip}")


def buscar_por_habilidad(agente: AgenteEstudianteTI):
    """Busca cursos por una habilidad específica."""
    print("\n🔍 BUSCAR CURSOS POR HABILIDAD")
    print("-" * 40)
    
    habilidad = input("¿Qué habilidad deseas aprender? ").strip()
    
    if not habilidad:
        print("❌ No ingresaste ninguna habilidad.")
        return
    
    cursos = agente.buscar_cursos_por_habilidad(habilidad)
    
    if cursos:
        print(f"\n📚 Cursos para aprender {habilidad}:")
        for curso in cursos:
            print(f"\n   📌 {curso['nombre']}")
            print(f"      Nivel: {curso['nivel']} | Duración: {curso['duracion_horas']}h")
            print(f"      {curso['descripcion']}")
    else:
        print(f"\n⚠️ No encontré cursos para '{habilidad}'.")
        print("   Prueba con: Python, JavaScript, SQL, Docker, Git, Linux, etc.")


def ver_cursos_por_categoria(agente: AgenteEstudianteTI):
    """Muestra los cursos organizados por categoría."""
    print("\n📚 CURSOS POR CATEGORÍA")
    print("-" * 40)
    
    # Obtener categorías únicas
    categorias = set(c.get("categoria") for c in agente.cursos.values())
    
    print("\nCategorías disponibles:")
    for i, cat in enumerate(sorted(categorias), 1):
        print(f"   {i}. {cat}")
    
    categoria_input = input("\n¿Qué categoría deseas ver? (nombre o número): ").strip()
    
    # Intentar convertir a número
    try:
        idx = int(categoria_input) - 1
        categoria = sorted(categorias)[idx]
    except (ValueError, IndexError):
        categoria = categoria_input
    
    cursos = agente.listar_cursos_por_categoria(categoria)
    
    if cursos:
        print(f"\n📚 Cursos en {categoria}:")
        for curso in cursos:
            print(f"\n   📌 {curso['nombre']}")
            print(f"      Nivel: {curso['nivel']} | Duración: {curso['duracion_horas']}h")
            print(f"      {curso['descripcion']}")
    else:
        print(f"\n⚠️ No encontré cursos en la categoría '{categoria}'.")


def resolver_duda(agente: AgenteEstudianteTI):
    """Ayuda a resolver dudas sobre un tema."""
    print("\n❓ RESOLVER DUDA")
    print("-" * 40)
    
    tema = input("¿Sobre qué tema tienes dudas? ").strip()
    
    if not tema:
        print("❌ No ingresaste ningún tema.")
        return
    
    resultado = agente.responder_duda(tema)
    
    print(f"\n{resultado['mensaje']}")
    
    if resultado['cursos_relacionados']:
        print("\n📚 Cursos que te pueden ayudar:")
        for curso in resultado['cursos_relacionados']:
            print(f"\n   📌 {curso['nombre']}")
            print(f"      {curso['descripcion']}")
            print(f"      Temas: {', '.join(curso['temas'])}")
    else:
        print("\n💡 Sugerencias:")
        print("   - Intenta con términos más generales")
        print("   - Ejemplos: POO, variables, funciones, base de datos, etc.")


def mostrar_info_agente(agente: AgenteEstudianteTI):
    """Muestra información sobre el agente."""
    resumen = agente.obtener_resumen_agente()
    
    print("\n" + "=" * 50)
    print("ℹ️  INFORMACIÓN DEL AGENTE")
    print("=" * 50)
    
    print(f"\n🤖 {resumen['nombre_agente']}")
    print(f"\n{resumen['descripcion']}")
    
    print(f"\n📊 Estadísticas:")
    print(f"   - Total de cursos: {resumen['total_cursos']}")
    print(f"   - Rutas predefinidas: {resumen['rutas_predefinidas_disponibles']}")
    
    print(f"\n📁 Categorías disponibles:")
    for cat in sorted(resumen['categorias_disponibles']):
        print(f"   - {cat}")
    
    print(f"\n🎯 Funcionalidades:")
    for func in resumen['funcionalidades']:
        print(f"   ✓ {func}")


def main():
    """Función principal de la interfaz interactiva."""
    agente = AgenteEstudianteTI()
    
    print("\n¡Bienvenido! 👋")
    print("Soy tu agente de aprendizaje para estudiantes de TI.")
    print("Estoy diseñado para ayudarte a aprender de manera ágil,")
    print("especialmente si tienes poco tiempo por trabajo u otras actividades.")
    
    while True:
        mostrar_menu_principal()
        opcion = input("Selecciona una opción (1-7): ").strip()
        
        if opcion == "1":
            ver_rutas_predefinidas(agente)
        elif opcion == "2":
            crear_ruta_personalizada(agente)
        elif opcion == "3":
            buscar_por_habilidad(agente)
        elif opcion == "4":
            ver_cursos_por_categoria(agente)
        elif opcion == "5":
            resolver_duda(agente)
        elif opcion == "6":
            mostrar_info_agente(agente)
        elif opcion == "7":
            print("\n¡Hasta luego! 👋 ¡Éxito en tu aprendizaje! 🚀\n")
            break
        else:
            print("\n❌ Opción no válida. Por favor selecciona 1-7.")
        
        input("\nPresiona Enter para continuar...")


if __name__ == "__main__":
    main()
