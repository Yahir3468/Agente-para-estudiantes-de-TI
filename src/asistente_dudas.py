"""
Asistente de resolución de dudas para estudiantes de TI.
"""

import random
import re
from typing import Dict, List, Any, Optional
from . import data_loader


class AsistenteDudas:
    """
    Asistente que ayuda a resolver dudas comunes de estudiantes de TI.
    Utiliza una base de conocimiento con preguntas frecuentes y puede
    sugerir recursos adicionales.
    """
    
    def __init__(self):
        self.base_conocimiento = data_loader.cargar_base_conocimiento()
        self.datos_cursos = data_loader.cargar_cursos()
    
    def buscar_respuesta(self, pregunta: str) -> Dict[str, Any]:
        """
        Busca una respuesta a la pregunta del estudiante.
        
        Args:
            pregunta: Pregunta o duda del estudiante.
            
        Returns:
            Dict con la respuesta encontrada o sugerencias.
        """
        pregunta_lower = pregunta.lower()
        
        # Buscar en la base de conocimiento
        respuestas_encontradas = self._buscar_en_base(pregunta_lower)
        
        if respuestas_encontradas:
            return {
                "encontrado": True,
                "respuestas": respuestas_encontradas,
                "cursos_relacionados": self._buscar_cursos_relacionados(pregunta_lower)
            }
        
        # Si no encuentra respuesta exacta, sugerir temas relacionados
        temas_sugeridos = self._sugerir_temas(pregunta_lower)
        cursos_sugeridos = self._buscar_cursos_relacionados(pregunta_lower)
        
        return {
            "encontrado": False,
            "mensaje": "No encontré una respuesta exacta, pero aquí hay recursos que podrían ayudarte:",
            "temas_relacionados": temas_sugeridos,
            "cursos_sugeridos": cursos_sugeridos
        }
    
    def _buscar_en_base(self, pregunta: str) -> List[Dict[str, str]]:
        """Busca respuestas en la base de conocimiento."""
        respuestas = []
        temas = self.base_conocimiento.get("temas", {})
        
        for categoria, subcategorias in temas.items():
            if isinstance(subcategorias, dict):
                for tema, contenido in subcategorias.items():
                    if isinstance(contenido, dict):
                        for nivel, faqs in contenido.items():
                            if isinstance(faqs, list):
                                for faq in faqs:
                                    if self._coincide_pregunta(pregunta, faq.get("pregunta", "")):
                                        respuestas.append({
                                            "categoria": categoria,
                                            "tema": tema,
                                            "nivel": nivel,
                                            "pregunta": faq["pregunta"],
                                            "respuesta": faq["respuesta"]
                                        })
                    elif isinstance(contenido, list):
                        for faq in contenido:
                            if self._coincide_pregunta(pregunta, faq.get("pregunta", "")):
                                respuestas.append({
                                    "categoria": categoria,
                                    "tema": tema,
                                    "pregunta": faq["pregunta"],
                                    "respuesta": faq["respuesta"]
                                })
            elif isinstance(subcategorias, list):
                for faq in subcategorias:
                    if self._coincide_pregunta(pregunta, faq.get("pregunta", "")):
                        respuestas.append({
                            "categoria": categoria,
                            "pregunta": faq["pregunta"],
                            "respuesta": faq["respuesta"]
                        })
        
        return respuestas
    
    def _coincide_pregunta(self, busqueda: str, pregunta_base: str) -> bool:
        """Verifica si la búsqueda coincide con una pregunta de la base."""
        pregunta_base_lower = pregunta_base.lower()
        
        # Palabras clave importantes para matching
        palabras_clave = self._extraer_palabras_clave(busqueda)
        
        coincidencias = sum(
            1 for palabra in palabras_clave
            if palabra in pregunta_base_lower
        )
        
        # Requiere al menos 2 palabras clave coincidentes o 50% de coincidencia
        umbral = max(2, len(palabras_clave) * 0.5)
        return coincidencias >= umbral
    
    def _extraer_palabras_clave(self, texto: str) -> List[str]:
        """Extrae palabras clave de un texto, ignorando palabras comunes."""
        palabras_comunes = {
            "que", "qué", "es", "un", "una", "el", "la", "los", "las",
            "como", "cómo", "para", "por", "en", "de", "del", "al",
            "y", "o", "a", "con", "sin", "cual", "cuál", "son", "hay"
        }
        
        # Eliminar signos de puntuación y convertir a minúsculas
        texto_limpio = re.sub(r'[^\w\s]', '', texto.lower())
        palabras = texto_limpio.split()
        return [p for p in palabras if len(p) > 2 and p not in palabras_comunes]
    
    def _buscar_cursos_relacionados(self, pregunta: str) -> List[Dict[str, Any]]:
        """Busca cursos relacionados con la pregunta."""
        cursos_relacionados = []
        palabras_clave = self._extraer_palabras_clave(pregunta)
        
        for categoria in self.datos_cursos["categorias"]:
            for curso in categoria["cursos"]:
                # Buscar en nombre, descripción y habilidades
                texto_curso = (
                    curso["nombre"].lower() + " " +
                    curso["descripcion"].lower() + " " +
                    " ".join(curso.get("habilidades", []))
                ).lower()
                
                coincidencias = sum(
                    1 for palabra in palabras_clave
                    if palabra in texto_curso
                )
                
                if coincidencias >= 1:
                    cursos_relacionados.append({
                        "id": curso["id"],
                        "nombre": curso["nombre"],
                        "nivel": curso["nivel"],
                        "duracion_horas": curso["duracion_horas"],
                        "categoria": categoria["nombre"],
                        "relevancia": coincidencias
                    })
        
        # Ordenar por relevancia
        cursos_relacionados.sort(key=lambda x: x["relevancia"], reverse=True)
        return cursos_relacionados[:5]  # Top 5 cursos
    
    def _sugerir_temas(self, pregunta: str) -> List[str]:
        """Sugiere temas relacionados basándose en la pregunta."""
        temas = []
        palabras_clave = self._extraer_palabras_clave(pregunta)
        
        mapeo_temas = {
            "python": ["Programación con Python", "Ciencia de Datos"],
            "javascript": ["Desarrollo Web", "Frontend"],
            "sql": ["Bases de Datos", "Consultas SQL"],
            "base": ["Bases de Datos"],
            "datos": ["Bases de Datos", "Ciencia de Datos"],
            "red": ["Redes y Comunicaciones"],
            "redes": ["Redes y Comunicaciones"],
            "ip": ["Redes y Comunicaciones"],
            "seguridad": ["Ciberseguridad"],
            "hack": ["Ciberseguridad", "Ethical Hacking"],
            "cloud": ["Computación en la Nube"],
            "nube": ["Computación en la Nube"],
            "docker": ["Contenedores", "DevOps"],
            "web": ["Desarrollo Web"],
            "api": ["Desarrollo Web", "Backend"]
        }
        
        for palabra in palabras_clave:
            for clave, temas_sugeridos in mapeo_temas.items():
                if clave in palabra:
                    temas.extend(temas_sugeridos)
        
        return list(set(temas))[:5]  # Eliminar duplicados y limitar a 5
    
    def obtener_tip_estudio(self) -> Dict[str, str]:
        """Retorna un tip de estudio aleatorio."""
        tips = self.base_conocimiento.get("tips_estudio", [])
        if tips:
            return random.choice(tips)
        return {
            "titulo": "Practica constantemente",
            "descripcion": "La práctica regular es clave para dominar cualquier habilidad técnica."
        }
    
    def obtener_todos_tips(self) -> List[Dict[str, str]]:
        """Retorna todos los tips de estudio disponibles."""
        return self.base_conocimiento.get("tips_estudio", [])
    
    def listar_temas_disponibles(self) -> Dict[str, List[str]]:
        """Lista todos los temas disponibles en la base de conocimiento."""
        temas_disponibles = {}
        temas = self.base_conocimiento.get("temas", {})
        
        for categoria, contenido in temas.items():
            if isinstance(contenido, dict):
                temas_disponibles[categoria] = list(contenido.keys())
            else:
                temas_disponibles[categoria] = ["general"]
        
        return temas_disponibles
