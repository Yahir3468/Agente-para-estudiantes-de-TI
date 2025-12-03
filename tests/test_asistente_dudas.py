"""
Pruebas unitarias para el asistente de dudas.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.asistente_dudas import AsistenteDudas


class TestAsistenteDudas:
    """Pruebas para el asistente de dudas."""
    
    @pytest.fixture
    def asistente(self):
        """Crea una instancia del asistente para las pruebas."""
        return AsistenteDudas()
    
    def test_inicializacion(self, asistente):
        """Verifica que el asistente se inicializa correctamente."""
        assert asistente.base_conocimiento is not None
        assert asistente.datos_cursos is not None
    
    def test_buscar_respuesta_existente(self, asistente):
        """Verifica búsqueda de respuesta existente."""
        resultado = asistente.buscar_respuesta("¿Qué es una variable en Python?")
        
        assert resultado["encontrado"] is True
        assert len(resultado["respuestas"]) > 0
    
    def test_buscar_respuesta_inexistente(self, asistente):
        """Verifica manejo de pregunta sin respuesta exacta."""
        resultado = asistente.buscar_respuesta("pregunta completamente aleatoria xyz123")
        
        assert resultado["encontrado"] is False
        assert "mensaje" in resultado
    
    def test_buscar_cursos_relacionados(self, asistente):
        """Verifica que encuentra cursos relacionados."""
        resultado = asistente.buscar_respuesta("python")
        
        assert "cursos_relacionados" in resultado or "cursos_sugeridos" in resultado
    
    def test_obtener_tip_estudio(self, asistente):
        """Verifica que retorna un tip de estudio."""
        tip = asistente.obtener_tip_estudio()
        
        assert "titulo" in tip
        assert "descripcion" in tip
    
    def test_obtener_todos_tips(self, asistente):
        """Verifica que retorna todos los tips."""
        tips = asistente.obtener_todos_tips()
        
        assert len(tips) > 0
        assert all("titulo" in t for t in tips)
    
    def test_listar_temas_disponibles(self, asistente):
        """Verifica listado de temas disponibles."""
        temas = asistente.listar_temas_disponibles()
        
        assert len(temas) > 0
        assert isinstance(temas, dict)
    
    def test_extraer_palabras_clave(self, asistente):
        """Verifica extracción de palabras clave."""
        palabras = asistente._extraer_palabras_clave("¿Qué es una variable en Python?")
        
        assert "variable" in palabras
        assert "python" in palabras
        # Palabras comunes deben excluirse
        assert "que" not in palabras
        assert "es" not in palabras
    
    def test_sugerir_temas_python(self, asistente):
        """Verifica sugerencia de temas para Python."""
        temas = asistente._sugerir_temas("python programación")
        
        assert len(temas) > 0
    
    def test_sugerir_temas_redes(self, asistente):
        """Verifica sugerencia de temas para redes."""
        temas = asistente._sugerir_temas("redes ip")
        
        assert any("Redes" in t for t in temas)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
