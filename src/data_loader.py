"""
Módulo de carga de datos para el agente de estudiantes de TI.
Maneja la carga de cursos y base de conocimiento desde archivos JSON.
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional


def get_data_path() -> Path:
    """Obtiene la ruta al directorio de datos."""
    current_file = Path(__file__).resolve()
    return current_file.parent.parent / "data"


def cargar_cursos() -> Dict[str, Any]:
    """
    Carga la matriz de cursos desde el archivo JSON.
    
    Returns:
        Dict con la estructura de cursos y perfiles de carrera.
    """
    data_path = get_data_path() / "cursos.json"
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)


def cargar_base_conocimiento() -> Dict[str, Any]:
    """
    Carga la base de conocimiento para resolver dudas.
    
    Returns:
        Dict con preguntas frecuentes y tips de estudio.
    """
    data_path = get_data_path() / "base_conocimiento.json"
    with open(data_path, "r", encoding="utf-8") as f:
        return json.load(f)


def obtener_curso_por_id(curso_id: str) -> Optional[Dict[str, Any]]:
    """
    Busca un curso específico por su ID.
    
    Args:
        curso_id: ID único del curso.
        
    Returns:
        Dict con información del curso o None si no existe.
    """
    datos = cargar_cursos()
    for categoria in datos["categorias"]:
        for curso in categoria["cursos"]:
            if curso["id"] == curso_id:
                return {**curso, "categoria": categoria["nombre"]}
    return None


def obtener_cursos_por_categoria(categoria_id: str) -> List[Dict[str, Any]]:
    """
    Obtiene todos los cursos de una categoría específica.
    
    Args:
        categoria_id: ID de la categoría.
        
    Returns:
        Lista de cursos de la categoría.
    """
    datos = cargar_cursos()
    for categoria in datos["categorias"]:
        if categoria["id"] == categoria_id:
            return categoria["cursos"]
    return []


def obtener_cursos_por_nivel(nivel: str) -> List[Dict[str, Any]]:
    """
    Obtiene todos los cursos de un nivel específico.
    
    Args:
        nivel: Nivel del curso (basico, intermedio, avanzado).
        
    Returns:
        Lista de cursos del nivel especificado.
    """
    datos = cargar_cursos()
    cursos = []
    for categoria in datos["categorias"]:
        for curso in categoria["cursos"]:
            if curso["nivel"] == nivel:
                cursos.append({**curso, "categoria": categoria["nombre"]})
    return cursos


def obtener_perfil_carrera(perfil_id: str) -> Optional[Dict[str, Any]]:
    """
    Obtiene un perfil de carrera por su ID.
    
    Args:
        perfil_id: ID del perfil de carrera.
        
    Returns:
        Dict con información del perfil o None si no existe.
    """
    datos = cargar_cursos()
    for perfil in datos["perfiles_carrera"]:
        if perfil["id"] == perfil_id:
            return perfil
    return None


def listar_categorias() -> List[Dict[str, str]]:
    """
    Lista todas las categorías disponibles.
    
    Returns:
        Lista con id, nombre y descripción de cada categoría.
    """
    datos = cargar_cursos()
    return [
        {
            "id": cat["id"],
            "nombre": cat["nombre"],
            "descripcion": cat["descripcion"]
        }
        for cat in datos["categorias"]
    ]


def listar_perfiles_carrera() -> List[Dict[str, str]]:
    """
    Lista todos los perfiles de carrera disponibles.
    
    Returns:
        Lista con id, nombre y descripción de cada perfil.
    """
    datos = cargar_cursos()
    return [
        {
            "id": perfil["id"],
            "nombre": perfil["nombre"],
            "descripcion": perfil["descripcion"]
        }
        for perfil in datos["perfiles_carrera"]
    ]


def obtener_ruta_aprendizaje(nivel: str) -> Optional[Dict[str, Any]]:
    """
    Obtiene una ruta de aprendizaje estructurada por nivel.
    
    Args:
        nivel: Nivel de la ruta (principiante, intermedio, avanzado).
        
    Returns:
        Dict con la ruta de aprendizaje completa o None si no existe.
    """
    datos = cargar_cursos()
    rutas = datos.get("rutas_aprendizaje", {})
    return rutas.get(nivel)


def listar_rutas_aprendizaje() -> List[Dict[str, Any]]:
    """
    Lista todas las rutas de aprendizaje disponibles.
    
    Returns:
        Lista con información básica de cada ruta.
    """
    datos = cargar_cursos()
    rutas = datos.get("rutas_aprendizaje", {})
    return [
        {
            "id": ruta["id"],
            "nombre": ruta["nombre"],
            "nivel": nivel,
            "duracion_semanas": ruta["duracion_semanas"],
            "horas_por_semana": ruta["horas_por_semana"],
            "objetivo": ruta["objetivo"]
        }
        for nivel, ruta in rutas.items()
    ]


def obtener_configuracion() -> Dict[str, Any]:
    """
    Obtiene la configuración general de las rutas.
    
    Returns:
        Dict con configuración (horas por semana, formato, etc.).
    """
    datos = cargar_cursos()
    return datos.get("configuracion", {
        "horas_por_semana": 4,
        "formato": "micro-learning",
        "duracion_actividad_minutos": "20-30",
        "duracion_ruta_semanas": 8
    })
