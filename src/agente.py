"""
Agente principal para estudiantes de Tecnologías de la Información.

Este agente ayuda a estudiantes de TI a:
1. Crear rutas de aprendizaje personalizadas
2. Resolver dudas sobre temas técnicos
3. Optimizar su tiempo de estudio

Diseñado especialmente para estudiantes que trabajan y tienen poco tiempo disponible.
"""

from typing import Dict, List, Any, Optional
from .generador_rutas import GeneradorRutas
from .asistente_dudas import AsistenteDudas
from . import data_loader


class AgenteEstudiantes:
    """
    Agente principal que coordina las funcionalidades de aprendizaje.
    """
    
    def __init__(self):
        self.generador_rutas = GeneradorRutas()
        self.asistente_dudas = AsistenteDudas()
        self.perfil_usuario: Dict[str, Any] = {}
    
    def configurar_perfil(
        self,
        nombre: str,
        horas_disponibles_semana: int,
        objetivo_carrera: Optional[str] = None,
        cursos_completados: Optional[List[str]] = None,
        nivel_experiencia: str = "principiante"
    ) -> Dict[str, Any]:
        """
        Configura el perfil del estudiante para personalizar recomendaciones.
        
        Args:
            nombre: Nombre del estudiante.
            horas_disponibles_semana: Horas que puede dedicar al estudio por semana.
            objetivo_carrera: ID del perfil de carrera objetivo (opcional).
            cursos_completados: Lista de IDs de cursos ya completados.
            nivel_experiencia: Nivel actual (principiante, intermedio, avanzado).
            
        Returns:
            Dict con el perfil configurado y recomendaciones iniciales.
        """
        self.perfil_usuario = {
            "nombre": nombre,
            "horas_semana": horas_disponibles_semana,
            "objetivo_carrera": objetivo_carrera,
            "cursos_completados": cursos_completados or [],
            "nivel_experiencia": nivel_experiencia
        }
        
        # Calcular recomendación de ritmo de estudio
        if horas_disponibles_semana < 5:
            ritmo = "microaprendizaje"
            sugerencia = "Con menos de 5 horas semanales, te recomiendo sesiones de 30 minutos máximo. Usa la técnica Pomodoro."
        elif horas_disponibles_semana < 10:
            ritmo = "moderado"
            sugerencia = "Con 5-10 horas semanales, puedes hacer buen progreso. Intenta estudiar 1-2 horas diarias."
        else:
            ritmo = "intensivo"
            sugerencia = "¡Excelente! Con más de 10 horas semanales puedes avanzar rápidamente. Alterna teoría con práctica."
        
        return {
            "perfil_guardado": True,
            "nombre": nombre,
            "ritmo_recomendado": ritmo,
            "sugerencia": sugerencia,
            "perfiles_carrera_disponibles": data_loader.listar_perfiles_carrera() if not objetivo_carrera else None
        }
    
    def obtener_ruta_aprendizaje(
        self,
        perfil_carrera: Optional[str] = None,
        habilidades: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Genera una ruta de aprendizaje personalizada.
        
        Args:
            perfil_carrera: ID del perfil de carrera (usa el del perfil si no se especifica).
            habilidades: Lista de habilidades específicas a aprender.
            
        Returns:
            Dict con la ruta de aprendizaje completa.
        """
        horas = self.perfil_usuario.get("horas_semana", 10)
        completados = self.perfil_usuario.get("cursos_completados", [])
        
        if habilidades:
            return self.generador_rutas.generar_ruta_por_habilidades(
                habilidades_objetivo=habilidades,
                horas_por_semana=horas,
                cursos_completados=completados
            )
        
        perfil_objetivo = perfil_carrera or self.perfil_usuario.get("objetivo_carrera")
        
        if not perfil_objetivo:
            return {
                "error": "No se especificó un objetivo. Por favor indica un perfil de carrera o habilidades.",
                "perfiles_disponibles": data_loader.listar_perfiles_carrera(),
                "tip": "Puedes usar: obtener_ruta_aprendizaje(perfil_carrera='desarrollador_web')"
            }
        
        return self.generador_rutas.generar_ruta_por_perfil(
            perfil_id=perfil_objetivo,
            horas_por_semana=horas,
            cursos_completados=completados
        )
    
    def obtener_ruta_rapida(
        self,
        categoria: str,
        horas_disponibles: int,
        nivel_maximo: str = "basico"
    ) -> Dict[str, Any]:
        """
        Genera una ruta rápida para aprender lo esencial de una categoría.
        Ideal para estudiantes con muy poco tiempo.
        
        Args:
            categoria: ID de la categoría (programacion, bases_datos, redes, etc.).
            horas_disponibles: Total de horas disponibles para invertir.
            nivel_maximo: Nivel máximo de cursos (basico, intermedio, avanzado).
            
        Returns:
            Dict con la ruta rápida optimizada.
        """
        return self.generador_rutas.generar_ruta_rapida(
            categoria_id=categoria,
            horas_disponibles=horas_disponibles,
            nivel=nivel_maximo
        )
    
    def resolver_duda(self, pregunta: str) -> Dict[str, Any]:
        """
        Responde una duda técnica del estudiante.
        
        Args:
            pregunta: Pregunta o duda del estudiante.
            
        Returns:
            Dict con la respuesta y recursos adicionales.
        """
        respuesta = self.asistente_dudas.buscar_respuesta(pregunta)
        
        # Agregar un tip de estudio si no encontró respuesta exacta
        if not respuesta.get("encontrado"):
            respuesta["tip_estudio"] = self.asistente_dudas.obtener_tip_estudio()
        
        return respuesta
    
    def obtener_resumen_diario(self) -> Dict[str, Any]:
        """
        Genera un resumen diario con sugerencias de estudio.
        
        Returns:
            Dict con el resumen y recomendaciones del día.
        """
        nombre = self.perfil_usuario.get("nombre", "Estudiante")
        horas = self.perfil_usuario.get("horas_semana", 10)
        objetivo = self.perfil_usuario.get("objetivo_carrera")
        
        # Calcular tiempo de estudio diario recomendado
        minutos_diarios = (horas * 60) // 7
        
        resumen = {
            "saludo": f"¡Hola {nombre}! Aquí está tu resumen del día.",
            "tiempo_estudio_sugerido": f"{minutos_diarios} minutos hoy",
            "tip_del_dia": self.asistente_dudas.obtener_tip_estudio()
        }
        
        if objetivo:
            perfil = data_loader.obtener_perfil_carrera(objetivo)
            if perfil:
                resumen["objetivo"] = perfil["nombre"]
                resumen["motivacion"] = f"Cada minuto de estudio te acerca más a ser {perfil['nombre']}."
        
        return resumen
    
    def listar_categorias(self) -> List[Dict[str, str]]:
        """Lista todas las categorías de cursos disponibles."""
        return data_loader.listar_categorias()
    
    def listar_perfiles_carrera(self) -> List[Dict[str, str]]:
        """Lista todos los perfiles de carrera disponibles."""
        return data_loader.listar_perfiles_carrera()
    
    def obtener_cursos_categoria(self, categoria_id: str) -> List[Dict[str, Any]]:
        """
        Obtiene todos los cursos de una categoría específica.
        
        Args:
            categoria_id: ID de la categoría.
            
        Returns:
            Lista de cursos de la categoría.
        """
        return data_loader.obtener_cursos_por_categoria(categoria_id)
    
    def marcar_curso_completado(self, curso_id: str) -> Dict[str, Any]:
        """
        Marca un curso como completado en el perfil del usuario.
        
        Args:
            curso_id: ID del curso completado.
            
        Returns:
            Dict con confirmación y progreso actualizado.
        """
        if "cursos_completados" not in self.perfil_usuario:
            self.perfil_usuario["cursos_completados"] = []
        
        if curso_id not in self.perfil_usuario["cursos_completados"]:
            self.perfil_usuario["cursos_completados"].append(curso_id)
            
            curso = data_loader.obtener_curso_por_id(curso_id)
            if curso:
                return {
                    "exito": True,
                    "mensaje": f"¡Felicidades! Has completado '{curso['nombre']}'",
                    "curso": curso["nombre"],
                    "total_completados": len(self.perfil_usuario["cursos_completados"])
                }
        
        return {
            "exito": False,
            "mensaje": "El curso ya estaba marcado como completado o no existe."
        }
    
    def obtener_progreso(self) -> Dict[str, Any]:
        """
        Obtiene el progreso actual del estudiante.
        
        Returns:
            Dict con estadísticas de progreso.
        """
        completados = self.perfil_usuario.get("cursos_completados", [])
        objetivo = self.perfil_usuario.get("objetivo_carrera")
        
        progreso = {
            "cursos_completados": len(completados),
            "lista_completados": []
        }
        
        # Obtener detalles de cursos completados
        horas_invertidas = 0
        for curso_id in completados:
            curso = data_loader.obtener_curso_por_id(curso_id)
            if curso:
                progreso["lista_completados"].append({
                    "nombre": curso["nombre"],
                    "categoria": curso["categoria"],
                    "horas": curso["duracion_horas"]
                })
                horas_invertidas += curso["duracion_horas"]
        
        progreso["horas_invertidas"] = horas_invertidas
        
        # Calcular progreso hacia objetivo si existe
        if objetivo:
            perfil = data_loader.obtener_perfil_carrera(objetivo)
            if perfil:
                cursos_objetivo = set(perfil["cursos_recomendados"])
                cursos_completados_objetivo = len(set(completados) & cursos_objetivo)
                progreso["objetivo"] = {
                    "nombre": perfil["nombre"],
                    "cursos_completados": cursos_completados_objetivo,
                    "cursos_totales": len(cursos_objetivo),
                    "porcentaje": round((cursos_completados_objetivo / len(cursos_objetivo)) * 100, 1)
                }
        
        return progreso
