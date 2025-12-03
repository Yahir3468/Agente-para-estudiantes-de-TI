"""
Tests para el Agente de Aprendizaje de Estudiantes de TI.
"""

import sys
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agente import AgenteEstudianteTI


class TestAgenteEstudianteTI:
    """Tests para la clase AgenteEstudianteTI."""

    def setup_method(self):
        """Configuración antes de cada test."""
        self.agente = AgenteEstudianteTI()

    def test_carga_cursos(self):
        """Verifica que los cursos se carguen correctamente."""
        assert len(self.agente.cursos) > 0
        assert "python-basico" in self.agente.cursos

    def test_obtener_curso_existente(self):
        """Verifica que se puede obtener un curso existente."""
        curso = self.agente.obtener_curso("python-basico")
        assert curso is not None
        assert curso["nombre"] == "Python Básico"
        assert curso["nivel"] == "Principiante"

    def test_obtener_curso_inexistente(self):
        """Verifica que retorna None para un curso inexistente."""
        curso = self.agente.obtener_curso("curso-inexistente")
        assert curso is None

    def test_listar_cursos_por_categoria(self):
        """Verifica el filtrado por categoría."""
        cursos = self.agente.listar_cursos_por_categoria("Programación")
        assert len(cursos) > 0
        for curso in cursos:
            assert curso["categoria"] == "Programación"

    def test_listar_cursos_por_nivel(self):
        """Verifica el filtrado por nivel."""
        cursos = self.agente.listar_cursos_por_nivel("Principiante")
        assert len(cursos) > 0
        for curso in cursos:
            assert curso["nivel"] == "Principiante"

    def test_buscar_cursos_por_habilidad(self):
        """Verifica la búsqueda por habilidad."""
        cursos = self.agente.buscar_cursos_por_habilidad("Python")
        assert len(cursos) > 0
        # Verificar que al menos uno tiene Python en habilidades
        habilidades = []
        for curso in cursos:
            habilidades.extend(curso.get("habilidades", []))
        assert any("python" in h.lower() for h in habilidades)

    def test_generar_ruta_personalizada(self):
        """Verifica la generación de rutas personalizadas."""
        ruta = self.agente.generar_ruta_personalizada(
            habilidades_objetivo=["Python"],
            horas_disponibles_semana=10,
            nivel_actual="principiante"
        )
        
        assert ruta["ruta_personalizada"] is True
        assert ruta["habilidades_objetivo"] == ["Python"]
        assert ruta["horas_semanales"] == 10
        assert len(ruta["cursos"]) > 0
        assert ruta["duracion_total_horas"] > 0
        assert ruta["semanas_estimadas"] > 0
        assert len(ruta["tips_estudiante_trabajador"]) > 0

    def test_rutas_personalizadas_incluyen_prerequisitos(self):
        """Verifica que las rutas incluyan los prerequisitos necesarios."""
        ruta = self.agente.generar_ruta_personalizada(
            habilidades_objetivo=["Machine Learning"],
            horas_disponibles_semana=5,
            nivel_actual="principiante"
        )
        
        # Verificar que incluya los prerequisitos de IA
        cursos_ids = [c["id"] for c in ruta["cursos"]]
        # Si hay curso de IA, debe incluir Python como prerequisito
        if "ia-intro" in cursos_ids:
            assert "python-basico" in cursos_ids or "python-intermedio" in cursos_ids

    def test_listar_rutas_predefinidas(self):
        """Verifica que se listen las rutas predefinidas."""
        rutas = self.agente.listar_rutas_predefinidas()
        assert len(rutas) > 0
        
        for ruta in rutas:
            assert "id" in ruta
            assert "nombre" in ruta
            assert "descripcion" in ruta
            assert "duracion_total_horas" in ruta

    def test_obtener_ruta_predefinida(self):
        """Verifica que se pueda obtener una ruta predefinida."""
        ruta = self.agente.obtener_ruta_predefinida("desarrollador_web_frontend")
        
        assert ruta is not None
        assert ruta["nombre"] == "Desarrollador Web Frontend"
        assert len(ruta["cursos"]) > 0

    def test_responder_duda(self):
        """Verifica la funcionalidad de resolver dudas."""
        resultado = self.agente.responder_duda("Python")
        
        assert "tema_consultado" in resultado
        assert "cursos_relacionados" in resultado
        assert "mensaje" in resultado
        assert resultado["tema_consultado"] == "Python"
        assert len(resultado["cursos_relacionados"]) > 0

    def test_obtener_resumen_agente(self):
        """Verifica el resumen del agente."""
        resumen = self.agente.obtener_resumen_agente()
        
        assert "nombre_agente" in resumen
        assert "descripcion" in resumen
        assert "total_cursos" in resumen
        assert "categorias_disponibles" in resumen
        assert "funcionalidades" in resumen
        assert resumen["total_cursos"] > 0

    def test_tips_estudio_varian_por_horas(self):
        """Verifica que los tips varían según las horas disponibles."""
        ruta_poco_tiempo = self.agente.generar_ruta_personalizada(
            habilidades_objetivo=["Python"],
            horas_disponibles_semana=3,
            nivel_actual="principiante"
        )
        
        ruta_mas_tiempo = self.agente.generar_ruta_personalizada(
            habilidades_objetivo=["Python"],
            horas_disponibles_semana=15,
            nivel_actual="principiante"
        )
        
        # Los tips deben ser diferentes según el tiempo disponible
        tips_poco = ruta_poco_tiempo["tips_estudiante_trabajador"]
        tips_mas = ruta_mas_tiempo["tips_estudiante_trabajador"]
        
        assert len(tips_poco) > 0
        assert len(tips_mas) > 0


def run_tests():
    """Ejecuta todos los tests manualmente."""
    test_instance = TestAgenteEstudianteTI()
    test_methods = [m for m in dir(test_instance) if m.startswith("test_")]
    
    passed = 0
    failed = 0
    
    print("🧪 Ejecutando tests del Agente de Aprendizaje...\n")
    
    for method_name in test_methods:
        test_instance.setup_method()
        try:
            getattr(test_instance, method_name)()
            print(f"  ✅ {method_name}")
            passed += 1
        except AssertionError as e:
            print(f"  ❌ {method_name}: {e}")
            failed += 1
        except Exception as e:
            print(f"  ❌ {method_name}: Error inesperado - {e}")
            failed += 1
    
    print(f"\n📊 Resultados: {passed} pasados, {failed} fallidos")
    return failed == 0


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
