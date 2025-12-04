"""
Generador de rutas de aprendizaje personalizadas para estudiantes de TI.
"""

from typing import Dict, List, Any, Optional
from . import data_loader


class GeneradorRutas:
    """
    Genera rutas de aprendizaje personalizadas basadas en:
    - Perfil de carrera objetivo
    - Tiempo disponible por semana (4 horas recomendado)
    - Nivel actual de conocimientos (principiante, intermedio, avanzado)
    - Cursos ya completados
    
    Las rutas están diseñadas para:
    - 4 horas por semana
    - Actividades en formato micro-learning (20-30 min)
    - Nivelado por experiencia
    - Énfasis en nube, infraestructura, datos, automatización
    """
    
    def __init__(self):
        self.datos_cursos = data_loader.cargar_cursos()
        self.cursos_por_id = self._indexar_cursos()
        self.configuracion = self.datos_cursos.get("configuracion", {
            "horas_por_semana": 4,
            "formato": "micro-learning",
            "duracion_actividad_minutos": "20-30",
            "duracion_ruta_semanas": 8
        })
    
    def _indexar_cursos(self) -> Dict[str, Dict[str, Any]]:
        """Crea un índice de cursos por ID para acceso rápido."""
        indice = {}
        for categoria in self.datos_cursos["categorias"]:
            for curso in categoria["cursos"]:
                indice[curso["id"]] = {**curso, "categoria": categoria["nombre"]}
        return indice
    
    def obtener_ruta_estructurada(
        self,
        nivel: str,
        semanas_completadas: Optional[List[int]] = None
    ) -> Dict[str, Any]:
        """
        Obtiene una ruta de aprendizaje estructurada de 8 semanas.
        
        Args:
            nivel: Nivel de la ruta (principiante, intermedio, avanzado).
            semanas_completadas: Lista de números de semanas ya completadas.
            
        Returns:
            Dict con la ruta estructurada semana por semana.
        """
        semanas_completadas = semanas_completadas or []
        rutas = self.datos_cursos.get("rutas_aprendizaje", {})
        ruta = rutas.get(nivel)
        
        if not ruta:
            return {
                "error": f"Ruta '{nivel}' no encontrada",
                "rutas_disponibles": list(rutas.keys())
            }
        
        # Construir la ruta con información de progreso
        semanas_detalle = []
        for semana_info in ruta["semanas"]:
            semana_num = semana_info["semana"]
            curso_id = semana_info.get("curso_id")
            curso_detalle = self.cursos_por_id.get(curso_id) if curso_id else None
            
            semana_detalle = {
                "semana": semana_num,
                "titulo": semana_info["titulo"],
                "duracion_sugerida_horas": semana_info["duracion_sugerida_horas"],
                "actividades": semana_info["actividades"],
                "mini_ejercicio": semana_info["mini_ejercicio"],
                "completada": semana_num in semanas_completadas,
                "es_proyecto_final": semana_info.get("es_proyecto_final", False)
            }
            
            if curso_detalle:
                semana_detalle["curso"] = {
                    "id": curso_id,
                    "nombre": curso_detalle["nombre"],
                    "habilidades": curso_detalle["habilidades"],
                    "url": curso_detalle.get("url", "")
                }
            
            if semana_info.get("entregables"):
                semana_detalle["entregables"] = semana_info["entregables"]
            
            if semana_info.get("componentes_proyecto"):
                semana_detalle["componentes_proyecto"] = semana_info["componentes_proyecto"]
            
            semanas_detalle.append(semana_detalle)
        
        progreso = len(semanas_completadas) / len(ruta["semanas"]) * 100
        
        return {
            "nombre": ruta["nombre"],
            "nivel": nivel,
            "objetivo": ruta["objetivo"],
            "duracion_semanas": ruta["duracion_semanas"],
            "horas_por_semana": ruta["horas_por_semana"],
            "formato": self.configuracion.get("formato", "micro-learning"),
            "duracion_actividad": self.configuracion.get("duracion_actividad_minutos", "20-30"),
            "semanas_completadas": len(semanas_completadas),
            "progreso_porcentaje": round(progreso, 1),
            "semanas": semanas_detalle,
            "requisitos_previos": ruta.get("requisitos_previos", []),
            "tips": self._obtener_tips_estudio()
        }
    
    def listar_rutas_disponibles(self) -> List[Dict[str, Any]]:
        """Lista todas las rutas de aprendizaje disponibles."""
        rutas = self.datos_cursos.get("rutas_aprendizaje", {})
        return [
            {
                "nivel": nivel,
                "nombre": ruta["nombre"],
                "objetivo": ruta["objetivo"],
                "duracion_semanas": ruta["duracion_semanas"],
                "horas_por_semana": ruta["horas_por_semana"],
                "requisitos_previos": ruta.get("requisitos_previos", [])
            }
            for nivel, ruta in rutas.items()
        ]
    
    def generar_ruta_por_perfil(
        self,
        perfil_id: str,
        horas_por_semana: int = 4,
        cursos_completados: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Genera una ruta de aprendizaje basada en un perfil de carrera.
        
        Args:
            perfil_id: ID del perfil de carrera objetivo.
            horas_por_semana: Horas disponibles para estudiar por semana.
            cursos_completados: Lista de IDs de cursos ya completados.
            
        Returns:
            Dict con la ruta de aprendizaje estructurada.
        """
        cursos_completados = cursos_completados or []
        perfil = data_loader.obtener_perfil_carrera(perfil_id)
        
        if not perfil:
            return {
                "error": f"Perfil '{perfil_id}' no encontrado",
                "perfiles_disponibles": data_loader.listar_perfiles_carrera()
            }
        
        # Obtener rutas recomendadas para el perfil
        rutas_recomendadas = perfil.get("rutas_recomendadas", [])
        cursos_clave = perfil.get("cursos_clave", [])
        
        # Obtener cursos del perfil que no estén completados
        cursos_pendientes = [
            curso_id for curso_id in cursos_clave
            if curso_id not in cursos_completados
        ]
        
        # Ordenar cursos respetando dependencias
        cursos_ordenados = self._ordenar_por_dependencias(cursos_pendientes)
        
        # Calcular duración y crear plan
        ruta = self._crear_plan_estudio(cursos_ordenados, horas_por_semana)
        
        return {
            "perfil": perfil["nombre"],
            "descripcion": perfil["descripcion"],
            "horas_semanales": horas_por_semana,
            "cursos_completados": len(cursos_completados),
            "cursos_pendientes": len(cursos_ordenados),
            "duracion_estimada_semanas": ruta["duracion_semanas"],
            "rutas_recomendadas": rutas_recomendadas,
            "ruta": ruta["fases"],
            "tips": self._obtener_tips_estudio()
        }
    
    def generar_ruta_por_habilidades(
        self,
        habilidades_objetivo: List[str],
        horas_por_semana: int = 4,
        cursos_completados: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Genera una ruta basada en habilidades específicas que se quieren aprender.
        
        Args:
            habilidades_objetivo: Lista de habilidades que se desean aprender.
            horas_por_semana: Horas disponibles para estudiar por semana.
            cursos_completados: Lista de IDs de cursos ya completados.
            
        Returns:
            Dict con la ruta de aprendizaje estructurada.
        """
        cursos_completados = cursos_completados or []
        cursos_relevantes = []
        
        # Buscar cursos que enseñen las habilidades objetivo
        for curso_id, curso in self.cursos_por_id.items():
            if curso_id in cursos_completados:
                continue
            for habilidad in curso.get("habilidades", []):
                if any(h.lower() in habilidad.lower() for h in habilidades_objetivo):
                    if curso_id not in cursos_relevantes:
                        cursos_relevantes.append(curso_id)
                    break
        
        if not cursos_relevantes:
            return {
                "error": "No se encontraron cursos para las habilidades especificadas",
                "habilidades_buscadas": habilidades_objetivo
            }
        
        # Agregar requisitos necesarios
        cursos_con_requisitos = self._agregar_requisitos(cursos_relevantes, cursos_completados)
        cursos_ordenados = self._ordenar_por_dependencias(cursos_con_requisitos)
        
        ruta = self._crear_plan_estudio(cursos_ordenados, horas_por_semana)
        
        return {
            "habilidades_objetivo": habilidades_objetivo,
            "horas_semanales": horas_por_semana,
            "cursos_encontrados": len(cursos_ordenados),
            "duracion_estimada_semanas": ruta["duracion_semanas"],
            "ruta": ruta["fases"],
            "tips": self._obtener_tips_estudio()
        }
    
    def generar_ruta_rapida(
        self,
        categoria_id: str,
        horas_disponibles: int,
        nivel: str = "principiante"
    ) -> Dict[str, Any]:
        """
        Genera una ruta rápida para aprender lo esencial de una categoría.
        Ideal para estudiantes con muy poco tiempo.
        
        Args:
            categoria_id: ID de la categoría a estudiar.
            horas_disponibles: Total de horas disponibles para invertir.
            nivel: Nivel máximo de cursos a incluir (principiante, intermedio, avanzado).
            
        Returns:
            Dict con la ruta rápida de aprendizaje.
        """
        niveles_orden = {"principiante": 1, "intermedio": 2, "avanzado": 3}
        nivel_max = niveles_orden.get(nivel, 1)
        
        cursos_categoria = data_loader.obtener_cursos_por_categoria(categoria_id)
        
        if not cursos_categoria:
            return {
                "error": f"Categoría '{categoria_id}' no encontrada",
                "categorias_disponibles": data_loader.listar_categorias()
            }
        
        # Filtrar por nivel y ordenar por duración
        cursos_filtrados = [
            c for c in cursos_categoria
            if niveles_orden.get(c["nivel"], 1) <= nivel_max
        ]
        cursos_filtrados.sort(key=lambda x: x["duracion_horas"])
        
        # Seleccionar cursos que quepan en el tiempo disponible
        cursos_seleccionados = []
        horas_acumuladas = 0
        
        for curso in cursos_filtrados:
            if horas_acumuladas + curso["duracion_horas"] <= horas_disponibles:
                cursos_seleccionados.append(curso)
                horas_acumuladas += curso["duracion_horas"]
        
        return {
            "categoria": categoria_id,
            "horas_disponibles": horas_disponibles,
            "horas_utilizadas": horas_acumuladas,
            "nivel_maximo": nivel,
            "cursos_seleccionados": [
                {
                    "nombre": c["nombre"],
                    "duracion_horas": c["duracion_horas"],
                    "nivel": c["nivel"],
                    "habilidades": c["habilidades"],
                    "mini_ejercicio": c.get("mini_ejercicio", "")
                }
                for c in cursos_seleccionados
            ],
            "recomendacion": self._generar_recomendacion_rapida(horas_disponibles)
        }
    
    def _ordenar_por_dependencias(self, curso_ids: List[str]) -> List[str]:
        """Ordena los cursos respetando sus requisitos previos."""
        # Crear grafo de dependencias
        visitados = set()
        ordenados = []
        
        def visitar(curso_id: str):
            if curso_id in visitados:
                return
            visitados.add(curso_id)
            
            curso = self.cursos_por_id.get(curso_id)
            if curso:
                for requisito in curso.get("requisitos", []):
                    if requisito in curso_ids:
                        visitar(requisito)
            
            ordenados.append(curso_id)
        
        for curso_id in curso_ids:
            visitar(curso_id)
        
        return ordenados
    
    def _agregar_requisitos(
        self,
        curso_ids: List[str],
        cursos_completados: List[str]
    ) -> List[str]:
        """Agrega los cursos requisitos que faltan."""
        todos_cursos = set(curso_ids)
        
        def agregar_requisitos_recursivo(curso_id: str):
            curso = self.cursos_por_id.get(curso_id)
            if curso:
                for requisito in curso.get("requisitos", []):
                    if requisito not in cursos_completados and requisito not in todos_cursos:
                        todos_cursos.add(requisito)
                        agregar_requisitos_recursivo(requisito)
        
        for curso_id in list(curso_ids):
            agregar_requisitos_recursivo(curso_id)
        
        return list(todos_cursos)
    
    def _crear_plan_estudio(
        self,
        curso_ids: List[str],
        horas_por_semana: int
    ) -> Dict[str, Any]:
        """Crea un plan de estudio dividido en fases."""
        fases = []
        cursos_fase_actual = []
        horas_fase = 0
        
        for curso_id in curso_ids:
            curso = self.cursos_por_id.get(curso_id)
            if not curso:
                continue
            
            duracion = curso["duracion_horas"]
            semanas_curso = max(1, duracion // horas_por_semana)
            
            cursos_fase_actual.append({
                "id": curso_id,
                "nombre": curso["nombre"],
                "nivel": curso["nivel"],
                "duracion_horas": duracion,
                "semanas_estimadas": semanas_curso,
                "habilidades": curso["habilidades"],
                "mini_ejercicio": curso.get("mini_ejercicio", ""),
                "url": curso.get("url", "")
            })
            horas_fase += duracion
            
            # Agrupar en fases de aproximadamente 16 horas (4 semanas a 4h/semana)
            if horas_fase >= 16 or curso_id == curso_ids[-1]:
                fases.append({
                    "fase": len(fases) + 1,
                    "cursos": cursos_fase_actual,
                    "horas_totales": horas_fase,
                    "semanas_estimadas": max(1, horas_fase // horas_por_semana)
                })
                cursos_fase_actual = []
                horas_fase = 0
        
        total_horas = sum(f["horas_totales"] for f in fases)
        total_semanas = max(1, total_horas // horas_por_semana)
        
        return {
            "fases": fases,
            "duracion_semanas": total_semanas,
            "horas_totales": total_horas
        }
    
    def _obtener_tips_estudio(self) -> List[Dict[str, str]]:
        """Obtiene tips de estudio de la base de conocimiento."""
        try:
            base = data_loader.cargar_base_conocimiento()
            return base.get("tips_estudio", [])[:3]  # Top 3 tips
        except Exception:
            return []
    
    def _generar_recomendacion_rapida(self, horas: int) -> str:
        """Genera una recomendación basada en el tiempo disponible."""
        if horas < 4:
            return "Con tan poco tiempo, enfócate en un solo concepto fundamental. Usa sesiones de 20-30 minutos (micro-learning)."
        elif horas < 8:
            return "Puedes cubrir los fundamentos básicos. Dedica 30 minutos diarios y practica los mini-ejercicios."
        elif horas < 16:
            return "Tienes tiempo suficiente para una buena base. Alterna teoría con práctica siguiendo el formato micro-learning."
        else:
            return "Excelente disponibilidad de tiempo. Puedes completar una ruta completa de 8 semanas. Incluye los proyectos finales."
