"""
Agente principal para estudiantes de Tecnologías de la Información.

Este agente ayuda a estudiantes de TI a:
1. Crear rutas de aprendizaje personalizadas de 8 semanas
2. Resolver dudas sobre temas técnicos
3. Optimizar su tiempo de estudio con formato micro-learning

Diseñado especialmente para estudiantes que trabajan y tienen poco tiempo disponible.
Rutas optimizadas para 4 horas por semana con actividades de 20-30 minutos.
"""

from typing import Dict, List, Any, Optional
from .generador_rutas import GeneradorRutas
from .asistente_dudas import AsistenteDudas
from . import data_loader


class AgenteEstudiantes:
    """
    Agente principal que coordina las funcionalidades de aprendizaje.
    
    Soporta rutas estructuradas de 8 semanas por nivel:
    - Principiante: Fundamentos de cloud, redes, seguridad y SQL
    - Intermedio: Infraestructura avanzada, Kubernetes, IaC
    - Avanzado: Arquitectura escalable, ML, Data Engineering
    """
    
    def __init__(self):
        self.generador_rutas = GeneradorRutas()
        self.asistente_dudas = AsistenteDudas()
        self.perfil_usuario: Dict[str, Any] = {}
    
    def configurar_perfil(
        self,
        nombre: str,
        horas_disponibles_semana: int = 4,
        objetivo_carrera: Optional[str] = None,
        cursos_completados: Optional[List[str]] = None,
        nivel_experiencia: str = "principiante",
        semanas_completadas: Optional[List[int]] = None
    ) -> Dict[str, Any]:
        """
        Configura el perfil del estudiante para personalizar recomendaciones.
        
        Args:
            nombre: Nombre del estudiante.
            horas_disponibles_semana: Horas que puede dedicar al estudio por semana (default: 4).
            objetivo_carrera: ID del perfil de carrera objetivo (opcional).
            cursos_completados: Lista de IDs de cursos ya completados.
            nivel_experiencia: Nivel actual (principiante, intermedio, avanzado).
            semanas_completadas: Lista de números de semanas ya completadas en la ruta actual.
            
        Returns:
            Dict con el perfil configurado y recomendaciones iniciales.
        """
        self.perfil_usuario = {
            "nombre": nombre,
            "horas_semana": horas_disponibles_semana,
            "objetivo_carrera": objetivo_carrera,
            "cursos_completados": cursos_completados or [],
            "nivel_experiencia": nivel_experiencia,
            "semanas_completadas": semanas_completadas or []
        }
        
        # Calcular recomendación de ritmo de estudio (optimizado para 4h/semana)
        if horas_disponibles_semana < 4:
            ritmo = "microaprendizaje"
            sugerencia = "Con menos de 4 horas semanales, te recomiendo sesiones de 20-30 minutos máximo. Enfócate en un solo tema por sesión."
        elif horas_disponibles_semana <= 6:
            ritmo = "óptimo"
            sugerencia = "¡Perfecto! Con 4-6 horas semanales puedes seguir la ruta estructurada. Divide en sesiones de 30 minutos."
        else:
            ritmo = "intensivo"
            sugerencia = "¡Excelente! Con más de 6 horas semanales puedes avanzar más rápido. Completa los mini-ejercicios y proyectos."
        
        return {
            "perfil_guardado": True,
            "nombre": nombre,
            "ritmo_recomendado": ritmo,
            "sugerencia": sugerencia,
            "nivel_actual": nivel_experiencia,
            "rutas_disponibles": self.generador_rutas.listar_rutas_disponibles(),
            "perfiles_carrera_disponibles": data_loader.listar_perfiles_carrera() if not objetivo_carrera else None
        }
    
    def obtener_ruta_estructurada(
        self,
        nivel: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Obtiene la ruta de aprendizaje estructurada de 8 semanas.
        
        Args:
            nivel: Nivel de la ruta (principiante, intermedio, avanzado).
                   Si no se especifica, usa el nivel del perfil.
            
        Returns:
            Dict con la ruta estructurada semana por semana.
        """
        nivel_ruta = nivel or self.perfil_usuario.get("nivel_experiencia", "principiante")
        semanas_completadas = self.perfil_usuario.get("semanas_completadas", [])
        
        return self.generador_rutas.obtener_ruta_estructurada(
            nivel=nivel_ruta,
            semanas_completadas=semanas_completadas
        )
    
    def listar_rutas_disponibles(self) -> List[Dict[str, Any]]:
        """Lista todas las rutas de aprendizaje estructuradas disponibles."""
        return self.generador_rutas.listar_rutas_disponibles()
    
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
        horas = self.perfil_usuario.get("horas_semana", 4)
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
                "rutas_estructuradas": self.generador_rutas.listar_rutas_disponibles(),
                "tip": "Puedes usar: obtener_ruta_estructurada(nivel='principiante') para la ruta de 8 semanas"
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
        nivel_maximo: str = "principiante"
    ) -> Dict[str, Any]:
        """
        Genera una ruta rápida para aprender lo esencial de una categoría.
        Ideal para estudiantes con muy poco tiempo.
        
        Args:
            categoria: ID de la categoría (google_cloud, seguridad_cloud, etc.).
            horas_disponibles: Total de horas disponibles para invertir.
            nivel_maximo: Nivel máximo de cursos (principiante, intermedio, avanzado).
            
        Returns:
            Dict con la ruta rápida optimizada.
        """
        return self.generador_rutas.generar_ruta_rapida(
            categoria_id=categoria,
            horas_disponibles=horas_disponibles,
            nivel=nivel_maximo
        )
    
    def marcar_semana_completada(self, numero_semana: int) -> Dict[str, Any]:
        """
        Marca una semana de la ruta como completada.
        
        Args:
            numero_semana: Número de la semana completada (1-8).
            
        Returns:
            Dict con confirmación y progreso actualizado.
        """
        if "semanas_completadas" not in self.perfil_usuario:
            self.perfil_usuario["semanas_completadas"] = []
        
        if numero_semana not in self.perfil_usuario["semanas_completadas"]:
            if 1 <= numero_semana <= 8:
                self.perfil_usuario["semanas_completadas"].append(numero_semana)
                self.perfil_usuario["semanas_completadas"].sort()
                
                nivel = self.perfil_usuario.get("nivel_experiencia", "principiante")
                progreso = len(self.perfil_usuario["semanas_completadas"]) / 8 * 100
                
                mensaje = f"¡Felicidades! Has completado la semana {numero_semana} de la ruta {nivel}."
                if numero_semana == 8:
                    mensaje = f"🎉 ¡FELICIDADES! Has completado la ruta {nivel} completa. ¡Excelente trabajo!"
                
                return {
                    "exito": True,
                    "mensaje": mensaje,
                    "semana_completada": numero_semana,
                    "total_semanas_completadas": len(self.perfil_usuario["semanas_completadas"]),
                    "progreso_porcentaje": round(progreso, 1),
                    "semanas_restantes": 8 - len(self.perfil_usuario["semanas_completadas"])
                }
            else:
                return {
                    "exito": False,
                    "mensaje": "El número de semana debe estar entre 1 y 8."
                }
        
        return {
            "exito": False,
            "mensaje": f"La semana {numero_semana} ya estaba marcada como completada."
        }
    
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
        horas = self.perfil_usuario.get("horas_semana", 4)
        objetivo = self.perfil_usuario.get("objetivo_carrera")
        nivel = self.perfil_usuario.get("nivel_experiencia", "principiante")
        semanas_completadas = self.perfil_usuario.get("semanas_completadas", [])
        
        # Calcular tiempo de estudio diario recomendado (formato micro-learning)
        minutos_diarios = (horas * 60) // 7
        
        resumen = {
            "saludo": f"¡Hola {nombre}! Aquí está tu resumen del día.",
            "tiempo_estudio_sugerido": f"{minutos_diarios} minutos hoy (sesiones de 20-30 min)",
            "formato": "micro-learning",
            "nivel_actual": nivel,
            "progreso_ruta": {
                "semanas_completadas": len(semanas_completadas),
                "semanas_totales": 8,
                "porcentaje": round(len(semanas_completadas) / 8 * 100, 1)
            },
            "tip_del_dia": self.asistente_dudas.obtener_tip_estudio()
        }
        
        # Sugerir próxima semana si hay semanas pendientes
        if len(semanas_completadas) < 8:
            proxima_semana = 1
            for i in range(1, 9):
                if i not in semanas_completadas:
                    proxima_semana = i
                    break
            resumen["proxima_semana"] = proxima_semana
        
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
        nivel = self.perfil_usuario.get("nivel_experiencia", "principiante")
        semanas_completadas = self.perfil_usuario.get("semanas_completadas", [])
        
        progreso = {
            "cursos_completados": len(completados),
            "lista_completados": [],
            "ruta_actual": {
                "nivel": nivel,
                "semanas_completadas": len(semanas_completadas),
                "semanas_totales": 8,
                "porcentaje": round(len(semanas_completadas) / 8 * 100, 1)
            }
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
                cursos_clave = set(perfil.get("cursos_clave", []))
                cursos_completados_objetivo = len(set(completados) & cursos_clave)
                total_cursos = len(cursos_clave) if cursos_clave else 1
                progreso["objetivo"] = {
                    "nombre": perfil["nombre"],
                    "cursos_completados": cursos_completados_objetivo,
                    "cursos_totales": total_cursos,
                    "porcentaje": round((cursos_completados_objetivo / total_cursos) * 100, 1)
                }
        
        return progreso
