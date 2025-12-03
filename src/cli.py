#!/usr/bin/env python3
"""
CLI interactiva para el Agente de Estudiantes de TI.

Uso:
    python -m src.cli
    python main.py
"""

import sys
from typing import Optional
from src.agente import AgenteEstudiantes


def imprimir_menu_principal():
    """Muestra el menú principal."""
    print("\n" + "=" * 60)
    print("🎓 AGENTE PARA ESTUDIANTES DE TI")
    print("=" * 60)
    print("\nOpciones disponibles:")
    print("  1. Configurar mi perfil")
    print("  2. Ver rutas de aprendizaje")
    print("  3. Generar ruta personalizada")
    print("  4. Ruta rápida (poco tiempo)")
    print("  5. Resolver una duda")
    print("  6. Ver mi progreso")
    print("  7. Marcar curso completado")
    print("  8. Tips de estudio")
    print("  9. Ver categorías y cursos")
    print("  0. Salir")
    print("-" * 60)


def imprimir_resultado(resultado: dict, indentacion: int = 0):
    """Imprime un resultado de forma legible."""
    espacios = "  " * indentacion
    
    for clave, valor in resultado.items():
        if isinstance(valor, dict):
            print(f"{espacios}📌 {clave}:")
            imprimir_resultado(valor, indentacion + 1)
        elif isinstance(valor, list):
            print(f"{espacios}📋 {clave}:")
            for i, item in enumerate(valor, 1):
                if isinstance(item, dict):
                    print(f"{espacios}  [{i}]")
                    imprimir_resultado(item, indentacion + 2)
                else:
                    print(f"{espacios}  - {item}")
        else:
            print(f"{espacios}• {clave}: {valor}")


def configurar_perfil(agente: AgenteEstudiantes):
    """Configura el perfil del estudiante."""
    print("\n📝 CONFIGURAR PERFIL")
    print("-" * 40)
    
    nombre = input("Tu nombre: ").strip() or "Estudiante"
    
    try:
        horas = int(input("Horas disponibles por semana para estudiar: ").strip() or "5")
    except ValueError:
        horas = 5
    
    print("\n¿Tienes un objetivo de carrera? Perfiles disponibles:")
    perfiles = agente.listar_perfiles_carrera()
    for i, p in enumerate(perfiles, 1):
        print(f"  {i}. {p['nombre']}")
    print("  0. No tengo objetivo definido aún")
    
    try:
        opcion = int(input("\nSelecciona (0-{}): ".format(len(perfiles))).strip() or "0")
        objetivo = perfiles[opcion - 1]["id"] if 0 < opcion <= len(perfiles) else None
    except (ValueError, IndexError):
        objetivo = None
    
    nivel = input("\nNivel de experiencia (principiante/intermedio/avanzado) [principiante]: ").strip() or "principiante"
    
    resultado = agente.configurar_perfil(
        nombre=nombre,
        horas_disponibles_semana=horas,
        objetivo_carrera=objetivo,
        nivel_experiencia=nivel
    )
    
    print("\n✅ Perfil configurado:")
    imprimir_resultado(resultado)


def ver_rutas_disponibles(agente: AgenteEstudiantes):
    """Muestra los perfiles de carrera disponibles."""
    print("\n🛤️ PERFILES DE CARRERA DISPONIBLES")
    print("-" * 40)
    
    perfiles = agente.listar_perfiles_carrera()
    for i, perfil in enumerate(perfiles, 1):
        print(f"\n{i}. {perfil['nombre']}")
        print(f"   📝 {perfil['descripcion']}")


def generar_ruta(agente: AgenteEstudiantes):
    """Genera una ruta de aprendizaje personalizada."""
    print("\n🎯 GENERAR RUTA DE APRENDIZAJE")
    print("-" * 40)
    
    print("\n¿Cómo quieres generar tu ruta?")
    print("  1. Por perfil de carrera")
    print("  2. Por habilidades específicas")
    
    opcion = input("\nSelecciona (1-2): ").strip()
    
    if opcion == "1":
        perfiles = agente.listar_perfiles_carrera()
        print("\nPerfiles disponibles:")
        for i, p in enumerate(perfiles, 1):
            print(f"  {i}. {p['nombre']}")
        
        try:
            sel = int(input("\nSelecciona un perfil: ").strip()) - 1
            if 0 <= sel < len(perfiles):
                resultado = agente.obtener_ruta_aprendizaje(perfil_carrera=perfiles[sel]["id"])
            else:
                print("❌ Selección inválida")
                return
        except ValueError:
            print("❌ Entrada inválida")
            return
    elif opcion == "2":
        habilidades_str = input("\nIngresa las habilidades separadas por coma (ej: python, flask, apis): ").strip()
        habilidades = [h.strip() for h in habilidades_str.split(",") if h.strip()]
        
        if not habilidades:
            print("❌ No ingresaste habilidades")
            return
        
        resultado = agente.obtener_ruta_aprendizaje(habilidades=habilidades)
    else:
        print("❌ Opción inválida")
        return
    
    print("\n📚 TU RUTA DE APRENDIZAJE:")
    imprimir_resultado(resultado)


def ruta_rapida(agente: AgenteEstudiantes):
    """Genera una ruta rápida para estudiantes con poco tiempo."""
    print("\n⚡ RUTA RÁPIDA")
    print("-" * 40)
    print("Ideal si tienes poco tiempo y quieres aprender lo esencial.\n")
    
    categorias = agente.listar_categorias()
    print("Categorías disponibles:")
    for i, cat in enumerate(categorias, 1):
        print(f"  {i}. {cat['nombre']}")
    
    try:
        sel = int(input("\nSelecciona una categoría: ").strip()) - 1
        if not 0 <= sel < len(categorias):
            print("❌ Selección inválida")
            return
        categoria = categorias[sel]["id"]
    except ValueError:
        print("❌ Entrada inválida")
        return
    
    try:
        horas = int(input("¿Cuántas horas puedes invertir en total? ").strip() or "10")
    except ValueError:
        horas = 10
    
    nivel = input("Nivel máximo (basico/intermedio/avanzado) [basico]: ").strip() or "basico"
    
    resultado = agente.obtener_ruta_rapida(categoria, horas, nivel)
    
    print("\n📚 TU RUTA RÁPIDA:")
    imprimir_resultado(resultado)


def resolver_duda(agente: AgenteEstudiantes):
    """Permite resolver una duda técnica."""
    print("\n❓ RESOLVER DUDA")
    print("-" * 40)
    
    pregunta = input("Escribe tu pregunta: ").strip()
    
    if not pregunta:
        print("❌ No ingresaste ninguna pregunta")
        return
    
    resultado = agente.resolver_duda(pregunta)
    
    print("\n💡 RESPUESTA:")
    imprimir_resultado(resultado)


def ver_progreso(agente: AgenteEstudiantes):
    """Muestra el progreso del estudiante."""
    print("\n📊 MI PROGRESO")
    print("-" * 40)
    
    resultado = agente.obtener_progreso()
    imprimir_resultado(resultado)


def marcar_completado(agente: AgenteEstudiantes):
    """Permite marcar un curso como completado."""
    print("\n✅ MARCAR CURSO COMPLETADO")
    print("-" * 40)
    
    categorias = agente.listar_categorias()
    print("Categorías:")
    for i, cat in enumerate(categorias, 1):
        print(f"  {i}. {cat['nombre']}")
    
    try:
        sel = int(input("\nSelecciona una categoría: ").strip()) - 1
        if not 0 <= sel < len(categorias):
            print("❌ Selección inválida")
            return
        
        cursos = agente.obtener_cursos_categoria(categorias[sel]["id"])
        print(f"\nCursos en {categorias[sel]['nombre']}:")
        for i, curso in enumerate(cursos, 1):
            print(f"  {i}. {curso['nombre']} ({curso['nivel']})")
        
        sel_curso = int(input("\nSelecciona el curso completado: ").strip()) - 1
        if not 0 <= sel_curso < len(cursos):
            print("❌ Selección inválida")
            return
        
        resultado = agente.marcar_curso_completado(cursos[sel_curso]["id"])
        imprimir_resultado(resultado)
        
    except ValueError:
        print("❌ Entrada inválida")


def ver_tips(agente: AgenteEstudiantes):
    """Muestra tips de estudio."""
    print("\n💡 TIPS DE ESTUDIO")
    print("-" * 40)
    
    tips = agente.asistente_dudas.obtener_todos_tips()
    for i, tip in enumerate(tips, 1):
        print(f"\n{i}. {tip['titulo']}")
        print(f"   📝 {tip['descripcion']}")


def ver_categorias_cursos(agente: AgenteEstudiantes):
    """Muestra todas las categorías y sus cursos."""
    print("\n📚 CATEGORÍAS Y CURSOS DISPONIBLES")
    print("-" * 40)
    
    categorias = agente.listar_categorias()
    
    for cat in categorias:
        print(f"\n📁 {cat['nombre']}")
        print(f"   {cat['descripcion']}")
        
        cursos = agente.obtener_cursos_categoria(cat["id"])
        for curso in cursos:
            emoji = "🟢" if curso["nivel"] == "basico" else "🟡" if curso["nivel"] == "intermedio" else "🔴"
            print(f"   {emoji} {curso['nombre']} - {curso['duracion_horas']}h ({curso['nivel']})")


def main():
    """Función principal del CLI."""
    agente = AgenteEstudiantes()
    
    print("\n" + "🎉" * 20)
    print("\n¡Bienvenido al Agente para Estudiantes de TI!")
    print("Estoy aquí para ayudarte a aprender de manera eficiente.")
    print("\n" + "🎉" * 20)
    
    while True:
        imprimir_menu_principal()
        
        try:
            opcion = input("Selecciona una opción: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n👋 ¡Hasta pronto! Sigue aprendiendo.")
            sys.exit(0)
        
        if opcion == "1":
            configurar_perfil(agente)
        elif opcion == "2":
            ver_rutas_disponibles(agente)
        elif opcion == "3":
            generar_ruta(agente)
        elif opcion == "4":
            ruta_rapida(agente)
        elif opcion == "5":
            resolver_duda(agente)
        elif opcion == "6":
            ver_progreso(agente)
        elif opcion == "7":
            marcar_completado(agente)
        elif opcion == "8":
            ver_tips(agente)
        elif opcion == "9":
            ver_categorias_cursos(agente)
        elif opcion == "0":
            print("\n👋 ¡Hasta pronto! Sigue aprendiendo.")
            sys.exit(0)
        else:
            print("\n❌ Opción no válida. Intenta de nuevo.")
        
        input("\n[Presiona Enter para continuar...]")


if __name__ == "__main__":
    main()
