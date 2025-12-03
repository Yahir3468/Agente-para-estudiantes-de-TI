"""
Agente de Aprendizaje para Estudiantes de TI

Este agente está diseñado para ayudar a estudiantes de Tecnologías de la Información
que trabajan y tienen poco tiempo para estudiar. El agente:
1. Crea rutas de aprendizaje personalizadas basadas en cursos autogestivos
2. Resuelve dudas sobre temas de TI
3. Sugiere recursos optimizados para aprendizaje ágil
"""

import json
from pathlib import Path
from typing import Optional


class AgenteEstudianteTI:
    """
    Agente inteligente para estudiantes de TI que genera rutas de aprendizaje
    personalizadas y responde dudas.
    """

    def __init__(self, cursos_path: Optional[str] = None):
        """
        Inicializa el agente cargando la matriz de cursos.
        
        Args:
            cursos_path: Ruta al archivo JSON con los cursos. Si no se proporciona,
                        usa la ruta por defecto.
        """
        if cursos_path is None:
            cursos_path = Path(__file__).parent.parent / "data" / "cursos.json"
        
        with open(cursos_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        self.cursos = {curso["id"]: curso for curso in data["cursos"]}
        self.rutas_predefinidas = data.get("rutas_predefinidas", {})
        
        # Mapeo de habilidades a cursos para búsqueda rápida
        self.habilidades_cursos = {}
        for curso_id, curso in self.cursos.items():
            for habilidad in curso.get("habilidades", []):
                habilidad_lower = habilidad.lower()
                if habilidad_lower not in self.habilidades_cursos:
                    self.habilidades_cursos[habilidad_lower] = []
                self.habilidades_cursos[habilidad_lower].append(curso_id)

    def obtener_curso(self, curso_id: str) -> Optional[dict]:
        """
        Obtiene la información de un curso por su ID.
        
        Args:
            curso_id: Identificador único del curso
            
        Returns:
            Diccionario con información del curso o None si no existe
        """
        return self.cursos.get(curso_id)

    def listar_cursos_por_categoria(self, categoria: str) -> list:
        """
        Lista todos los cursos de una categoría específica.
        
        Args:
            categoria: Nombre de la categoría
            
        Returns:
            Lista de cursos que pertenecen a la categoría
        """
        return [
            curso for curso in self.cursos.values()
            if curso.get("categoria", "").lower() == categoria.lower()
        ]

    def listar_cursos_por_nivel(self, nivel: str) -> list:
        """
        Lista todos los cursos de un nivel específico.
        
        Args:
            nivel: Nivel del curso (Principiante, Intermedio, Avanzado)
            
        Returns:
            Lista de cursos que pertenecen al nivel
        """
        return [
            curso for curso in self.cursos.values()
            if curso.get("nivel", "").lower() == nivel.lower()
        ]

    def buscar_cursos_por_habilidad(self, habilidad: str) -> list:
        """
        Busca cursos que enseñen una habilidad específica.
        
        Args:
            habilidad: Habilidad que se desea aprender
            
        Returns:
            Lista de cursos que enseñan la habilidad
        """
        habilidad_lower = habilidad.lower()
        curso_ids = self.habilidades_cursos.get(habilidad_lower, [])
        
        # También buscar en habilidades que contengan el término
        for hab, ids in self.habilidades_cursos.items():
            if habilidad_lower in hab and hab not in self.habilidades_cursos.get(habilidad_lower, []):
                curso_ids.extend([id_ for id_ in ids if id_ not in curso_ids])
        
        return [self.cursos[id_] for id_ in curso_ids if id_ in self.cursos]

    def _resolver_prerequisitos(self, curso_id: str, visitados: set = None) -> list:
        """
        Resuelve recursivamente los prerequisitos de un curso.
        
        Args:
            curso_id: ID del curso
            visitados: Conjunto de cursos ya visitados (para evitar ciclos)
            
        Returns:
            Lista ordenada de cursos prerequisitos
        """
        if visitados is None:
            visitados = set()
        
        if curso_id in visitados:
            return []
        
        visitados.add(curso_id)
        curso = self.cursos.get(curso_id)
        
        if not curso:
            return []
        
        prerequisitos = []
        for prereq_id in curso.get("prerequisitos", []):
            prerequisitos.extend(self._resolver_prerequisitos(prereq_id, visitados))
            if prereq_id not in [c["id"] for c in prerequisitos]:
                prereq = self.cursos.get(prereq_id)
                if prereq:
                    prerequisitos.append(prereq)
        
        return prerequisitos

    def generar_ruta_personalizada(
        self,
        habilidades_objetivo: list,
        horas_disponibles_semana: int = 5,
        nivel_actual: str = "principiante"
    ) -> dict:
        """
        Genera una ruta de aprendizaje personalizada basada en las habilidades deseadas.
        
        Args:
            habilidades_objetivo: Lista de habilidades que el estudiante quiere aprender
            horas_disponibles_semana: Horas semanales disponibles para estudiar
            nivel_actual: Nivel actual del estudiante
            
        Returns:
            Diccionario con la ruta de aprendizaje personalizada
        """
        cursos_ruta = []
        cursos_agregados = set()
        
        # Mapeo de niveles para ordenamiento
        niveles = {"principiante": 1, "intermedio": 2, "avanzado": 3}
        nivel_estudiante = niveles.get(nivel_actual.lower(), 1)
        
        for habilidad in habilidades_objetivo:
            cursos_habilidad = self.buscar_cursos_por_habilidad(habilidad)
            
            for curso in cursos_habilidad:
                curso_id = curso["id"]
                if curso_id in cursos_agregados:
                    continue
                
                # Agregar prerequisitos primero
                prerequisitos = self._resolver_prerequisitos(curso_id)
                for prereq in prerequisitos:
                    if prereq["id"] not in cursos_agregados:
                        cursos_ruta.append(prereq)
                        cursos_agregados.add(prereq["id"])
                
                # Agregar el curso
                cursos_ruta.append(curso)
                cursos_agregados.add(curso_id)
        
        # Ordenar por nivel
        cursos_ruta.sort(
            key=lambda c: niveles.get(c.get("nivel", "").lower(), 1)
        )
        
        # Calcular tiempos
        duracion_total = sum(c.get("duracion_horas", 0) for c in cursos_ruta)
        semanas_estimadas = (
            duracion_total / horas_disponibles_semana if horas_disponibles_semana > 0 else 0
        )
        
        return {
            "ruta_personalizada": True,
            "habilidades_objetivo": habilidades_objetivo,
            "nivel_actual": nivel_actual,
            "cursos": cursos_ruta,
            "duracion_total_horas": duracion_total,
            "horas_semanales": horas_disponibles_semana,
            "semanas_estimadas": round(semanas_estimadas, 1),
            "tips_estudiante_trabajador": self._generar_tips_estudio(horas_disponibles_semana)
        }

    def obtener_ruta_predefinida(self, nombre_ruta: str) -> Optional[dict]:
        """
        Obtiene una ruta de aprendizaje predefinida.
        
        Args:
            nombre_ruta: Identificador de la ruta predefinida
            
        Returns:
            Diccionario con la ruta de aprendizaje o None si no existe
        """
        ruta = self.rutas_predefinidas.get(nombre_ruta)
        if not ruta:
            return None
        
        cursos_detalle = []
        for curso_id in ruta.get("cursos", []):
            curso = self.cursos.get(curso_id)
            if curso:
                cursos_detalle.append(curso)
        
        return {
            "nombre": ruta.get("nombre"),
            "descripcion": ruta.get("descripcion"),
            "cursos": cursos_detalle,
            "duracion_total_horas": ruta.get("duracion_total_horas", 0)
        }

    def listar_rutas_predefinidas(self) -> list:
        """
        Lista todas las rutas de aprendizaje predefinidas disponibles.
        
        Returns:
            Lista de rutas predefinidas con información básica
        """
        return [
            {
                "id": ruta_id,
                "nombre": ruta.get("nombre"),
                "descripcion": ruta.get("descripcion"),
                "duracion_total_horas": ruta.get("duracion_total_horas", 0)
            }
            for ruta_id, ruta in self.rutas_predefinidas.items()
        ]

    def _generar_tips_estudio(self, horas_semana: int) -> list:
        """
        Genera consejos de estudio personalizados según el tiempo disponible.
        
        Args:
            horas_semana: Horas disponibles por semana
            
        Returns:
            Lista de consejos para optimizar el tiempo de estudio
        """
        tips = [
            "📚 Divide tu tiempo de estudio en sesiones cortas de 25-30 minutos (técnica Pomodoro).",
            "🎯 Enfócate en un solo tema a la vez para mayor retención.",
            "📝 Toma notas breves y crea resúmenes propios.",
            "💻 Practica activamente: programa, no solo leas.",
        ]
        
        if horas_semana <= 5:
            tips.extend([
                "⚡ Con poco tiempo, prioriza la práctica sobre la teoría.",
                "📱 Aprovecha tiempos muertos (transporte) para repasar notas.",
                "🌙 Estudia en tu momento de mayor concentración del día."
            ])
        elif horas_semana <= 10:
            tips.extend([
                "📅 Establece horarios fijos de estudio para crear hábito.",
                "🔄 Alterna entre teoría y práctica cada sesión."
            ])
        else:
            tips.extend([
                "🚀 Con más tiempo, puedes profundizar en proyectos prácticos.",
                "👥 Considera unirte a comunidades de estudio."
            ])
        
        return tips

    def responder_duda(self, tema: str) -> dict:
        """
        Busca recursos relacionados con un tema o duda específica.
        
        Args:
            tema: Tema sobre el cual el estudiante tiene dudas
            
        Returns:
            Diccionario con cursos y recursos relacionados
        """
        tema_lower = tema.lower()
        cursos_relacionados = []
        
        for curso in self.cursos.values():
            # Buscar en nombre, descripción y temas del curso
            if (tema_lower in curso.get("nombre", "").lower() or
                tema_lower in curso.get("descripcion", "").lower() or
                any(tema_lower in t.lower() for t in curso.get("temas", []))):
                cursos_relacionados.append(curso)
        
        if not cursos_relacionados:
            # Buscar por habilidades si no hay resultados directos
            cursos_relacionados = self.buscar_cursos_por_habilidad(tema)
        
        return {
            "tema_consultado": tema,
            "cursos_relacionados": cursos_relacionados,
            "mensaje": (
                f"Encontré {len(cursos_relacionados)} curso(s) relacionado(s) con '{tema}'."
                if cursos_relacionados
                else f"No encontré cursos específicos sobre '{tema}'. Intenta con otros términos."
            )
        }

    def obtener_resumen_agente(self) -> dict:
        """
        Obtiene un resumen de las capacidades del agente y cursos disponibles.
        
        Returns:
            Diccionario con información resumida del agente
        """
        categorias = set(c.get("categoria") for c in self.cursos.values())
        niveles = set(c.get("nivel") for c in self.cursos.values())
        
        return {
            "nombre_agente": "Agente de Aprendizaje para Estudiantes de TI",
            "descripcion": (
                "Soy un agente diseñado para ayudar a estudiantes de TI que trabajan "
                "y tienen poco tiempo para estudiar. Puedo crear rutas de aprendizaje "
                "personalizadas y ayudarte a resolver dudas."
            ),
            "total_cursos": len(self.cursos),
            "categorias_disponibles": list(categorias),
            "niveles_disponibles": list(niveles),
            "rutas_predefinidas_disponibles": len(self.rutas_predefinidas),
            "funcionalidades": [
                "Generar rutas de aprendizaje personalizadas",
                "Mostrar rutas predefinidas para diferentes carreras",
                "Buscar cursos por habilidad, categoría o nivel",
                "Responder dudas sobre temas de TI",
                "Proporcionar tips de estudio para estudiantes que trabajan"
            ]
        }


def main():
    """Función principal para demostrar el uso del agente."""
    agente = AgenteEstudianteTI()
    
    print("=" * 60)
    print("🎓 AGENTE DE APRENDIZAJE PARA ESTUDIANTES DE TI")
    print("=" * 60)
    
    # Mostrar resumen del agente
    resumen = agente.obtener_resumen_agente()
    print(f"\n📋 {resumen['descripcion']}")
    print(f"\n📊 Estadísticas:")
    print(f"   - Total de cursos: {resumen['total_cursos']}")
    print(f"   - Categorías: {', '.join(resumen['categorias_disponibles'])}")
    print(f"   - Rutas predefinidas: {resumen['rutas_predefinidas_disponibles']}")
    
    # Mostrar rutas predefinidas
    print("\n" + "=" * 60)
    print("🛤️  RUTAS DE APRENDIZAJE PREDEFINIDAS")
    print("=" * 60)
    
    for ruta in agente.listar_rutas_predefinidas():
        print(f"\n📌 {ruta['nombre']}")
        print(f"   {ruta['descripcion']}")
        print(f"   ⏱️  Duración: {ruta['duracion_total_horas']} horas")
    
    # Ejemplo de ruta personalizada
    print("\n" + "=" * 60)
    print("🎯 EJEMPLO: RUTA PERSONALIZADA")
    print("=" * 60)
    
    ruta_personalizada = agente.generar_ruta_personalizada(
        habilidades_objetivo=["Python", "APIs"],
        horas_disponibles_semana=5,
        nivel_actual="principiante"
    )
    
    print(f"\n🎯 Habilidades objetivo: {', '.join(ruta_personalizada['habilidades_objetivo'])}")
    print(f"⏰ Horas semanales disponibles: {ruta_personalizada['horas_semanales']}")
    print(f"📅 Semanas estimadas: {ruta_personalizada['semanas_estimadas']}")
    
    print("\n📚 Cursos en tu ruta:")
    for i, curso in enumerate(ruta_personalizada['cursos'], 1):
        print(f"   {i}. {curso['nombre']} ({curso['nivel']}) - {curso['duracion_horas']}h")
    
    print("\n💡 Tips para estudiantes que trabajan:")
    for tip in ruta_personalizada['tips_estudiante_trabajador'][:3]:
        print(f"   {tip}")
    
    print("\n" + "=" * 60)
    print("✅ ¡Listo para ayudarte a aprender de manera ágil!")
    print("=" * 60)


if __name__ == "__main__":
    main()
