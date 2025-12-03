"""
Pruebas unitarias para el agente principal.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agente import AgenteEstudiantes


class TestAgenteEstudiantes:
    """Pruebas para el agente principal."""
    
    @pytest.fixture
    def agente(self):
        """Crea una instancia del agente para las pruebas."""
        return AgenteEstudiantes()
    
    def test_inicializacion(self, agente):
        """Verifica que el agente se inicializa correctamente."""
        assert agente.generador_rutas is not None
        assert agente.asistente_dudas is not None
        assert agente.perfil_usuario == {}
    
    def test_configurar_perfil(self, agente):
        """Verifica configuración del perfil de usuario."""
        resultado = agente.configurar_perfil(
            nombre="Test",
            horas_disponibles_semana=10,
            objetivo_carrera="desarrollador_web",
            nivel_experiencia="principiante"
        )
        
        assert resultado["perfil_guardado"] is True
        assert resultado["nombre"] == "Test"
        assert "ritmo_recomendado" in resultado
        assert "sugerencia" in resultado
        
        # Verificar que se guardó el perfil
        assert agente.perfil_usuario["nombre"] == "Test"
        assert agente.perfil_usuario["horas_semana"] == 10
    
    def test_configurar_perfil_poco_tiempo(self, agente):
        """Verifica recomendaciones para poco tiempo disponible."""
        resultado = agente.configurar_perfil(
            nombre="Ocupado",
            horas_disponibles_semana=3
        )
        
        assert resultado["ritmo_recomendado"] == "microaprendizaje"
    
    def test_configurar_perfil_mucho_tiempo(self, agente):
        """Verifica recomendaciones para mucho tiempo disponible."""
        resultado = agente.configurar_perfil(
            nombre="Intensivo",
            horas_disponibles_semana=15
        )
        
        assert resultado["ritmo_recomendado"] == "intensivo"
    
    def test_obtener_ruta_sin_objetivo(self, agente):
        """Verifica manejo cuando no hay objetivo configurado."""
        resultado = agente.obtener_ruta_aprendizaje()
        
        assert "error" in resultado
        assert "perfiles_disponibles" in resultado
    
    def test_obtener_ruta_con_perfil(self, agente):
        """Verifica obtención de ruta con perfil configurado."""
        agente.configurar_perfil(
            nombre="Test",
            horas_disponibles_semana=10,
            objetivo_carrera="desarrollador_web"
        )
        
        resultado = agente.obtener_ruta_aprendizaje()
        
        assert "error" not in resultado
        assert "ruta" in resultado
    
    def test_obtener_ruta_por_habilidades(self, agente):
        """Verifica obtención de ruta por habilidades."""
        resultado = agente.obtener_ruta_aprendizaje(habilidades=["python", "flask"])
        
        assert "error" not in resultado
        assert "ruta" in resultado
    
    def test_obtener_ruta_rapida(self, agente):
        """Verifica obtención de ruta rápida."""
        resultado = agente.obtener_ruta_rapida("programacion", 15, "basico")
        
        assert "error" not in resultado
        assert "cursos_seleccionados" in resultado
    
    def test_resolver_duda(self, agente):
        """Verifica resolución de duda."""
        resultado = agente.resolver_duda("¿Qué es Python?")
        
        assert "encontrado" in resultado or "mensaje" in resultado
    
    def test_obtener_resumen_diario(self, agente):
        """Verifica generación del resumen diario."""
        agente.configurar_perfil(nombre="Test", horas_disponibles_semana=7)
        
        resumen = agente.obtener_resumen_diario()
        
        assert "saludo" in resumen
        assert "tiempo_estudio_sugerido" in resumen
        assert "tip_del_dia" in resumen
    
    def test_listar_categorias(self, agente):
        """Verifica listado de categorías."""
        categorias = agente.listar_categorias()
        
        assert len(categorias) > 0
    
    def test_listar_perfiles_carrera(self, agente):
        """Verifica listado de perfiles de carrera."""
        perfiles = agente.listar_perfiles_carrera()
        
        assert len(perfiles) > 0
    
    def test_marcar_curso_completado(self, agente):
        """Verifica marcado de curso como completado."""
        agente.configurar_perfil(nombre="Test", horas_disponibles_semana=10)
        
        resultado = agente.marcar_curso_completado("prog-001")
        
        assert resultado["exito"] is True
        assert "prog-001" in agente.perfil_usuario["cursos_completados"]
    
    def test_marcar_curso_completado_duplicado(self, agente):
        """Verifica que no duplica cursos completados."""
        agente.configurar_perfil(nombre="Test", horas_disponibles_semana=10)
        
        agente.marcar_curso_completado("prog-001")
        resultado = agente.marcar_curso_completado("prog-001")
        
        assert resultado["exito"] is False
    
    def test_obtener_progreso(self, agente):
        """Verifica obtención de progreso."""
        agente.configurar_perfil(
            nombre="Test",
            horas_disponibles_semana=10,
            objetivo_carrera="desarrollador_web"
        )
        agente.marcar_curso_completado("prog-001")
        
        progreso = agente.obtener_progreso()
        
        assert progreso["cursos_completados"] == 1
        assert progreso["horas_invertidas"] > 0
        assert "objetivo" in progreso


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
