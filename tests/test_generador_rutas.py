"""
Pruebas unitarias para el generador de rutas de aprendizaje.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.generador_rutas import GeneradorRutas


class TestGeneradorRutas:
    """Pruebas para el generador de rutas."""
    
    @pytest.fixture
    def generador(self):
        """Crea una instancia del generador para las pruebas."""
        return GeneradorRutas()
    
    def test_inicializacion(self, generador):
        """Verifica que el generador se inicializa correctamente."""
        assert generador.datos_cursos is not None
        assert len(generador.cursos_por_id) > 0
    
    def test_generar_ruta_por_perfil_existente(self, generador):
        """Verifica generación de ruta para perfil existente."""
        ruta = generador.generar_ruta_por_perfil("desarrollador_web", horas_por_semana=10)
        
        assert "error" not in ruta
        assert "perfil" in ruta
        assert "ruta" in ruta
        assert "duracion_estimada_semanas" in ruta
        assert len(ruta["ruta"]) > 0
    
    def test_generar_ruta_por_perfil_inexistente(self, generador):
        """Verifica manejo de perfil inexistente."""
        ruta = generador.generar_ruta_por_perfil("perfil_inexistente")
        
        assert "error" in ruta
        assert "perfiles_disponibles" in ruta
    
    def test_generar_ruta_con_cursos_completados(self, generador):
        """Verifica que excluye cursos ya completados."""
        ruta_sin_completados = generador.generar_ruta_por_perfil(
            "desarrollador_web",
            cursos_completados=[]
        )
        
        ruta_con_completados = generador.generar_ruta_por_perfil(
            "desarrollador_web",
            cursos_completados=["prog-001", "prog-002"]
        )
        
        assert ruta_con_completados["cursos_pendientes"] < ruta_sin_completados["cursos_pendientes"]
    
    def test_generar_ruta_por_habilidades(self, generador):
        """Verifica generación de ruta por habilidades."""
        ruta = generador.generar_ruta_por_habilidades(
            habilidades_objetivo=["python", "flask"],
            horas_por_semana=10
        )
        
        assert "error" not in ruta
        assert "habilidades_objetivo" in ruta
        assert "ruta" in ruta
    
    def test_generar_ruta_por_habilidades_inexistentes(self, generador):
        """Verifica manejo de habilidades no encontradas."""
        ruta = generador.generar_ruta_por_habilidades(
            habilidades_objetivo=["habilidad_inexistente_xyz"],
            horas_por_semana=10
        )
        
        assert "error" in ruta
    
    def test_generar_ruta_rapida(self, generador):
        """Verifica generación de ruta rápida."""
        ruta = generador.generar_ruta_rapida(
            categoria_id="programacion",
            horas_disponibles=20,
            nivel="basico"
        )
        
        assert "error" not in ruta
        assert "cursos_seleccionados" in ruta
        assert ruta["horas_utilizadas"] <= 20
    
    def test_generar_ruta_rapida_categoria_inexistente(self, generador):
        """Verifica manejo de categoría inexistente."""
        ruta = generador.generar_ruta_rapida(
            categoria_id="inexistente",
            horas_disponibles=20
        )
        
        assert "error" in ruta
        assert "categorias_disponibles" in ruta
    
    def test_ordenar_por_dependencias(self, generador):
        """Verifica que los cursos se ordenan respetando dependencias."""
        # prog-002 depende de prog-001
        cursos = ["prog-002", "prog-001"]
        ordenados = generador._ordenar_por_dependencias(cursos)
        
        # prog-001 debe aparecer antes que prog-002
        assert ordenados.index("prog-001") < ordenados.index("prog-002")
    
    def test_horas_semanales_afectan_duracion(self, generador):
        """Verifica que más horas semanales reducen la duración."""
        ruta_5h = generador.generar_ruta_por_perfil("desarrollador_web", horas_por_semana=5)
        ruta_20h = generador.generar_ruta_por_perfil("desarrollador_web", horas_por_semana=20)
        
        assert ruta_5h["duracion_estimada_semanas"] > ruta_20h["duracion_estimada_semanas"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
