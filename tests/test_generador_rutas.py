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
        assert "horas_por_semana" in generador.configuracion
    
    def test_obtener_ruta_estructurada(self, generador):
        """Verifica obtención de ruta estructurada de 8 semanas."""
        ruta = generador.obtener_ruta_estructurada("principiante")
        
        assert "error" not in ruta
        assert "semanas" in ruta
        assert len(ruta["semanas"]) == 8
        assert ruta["duracion_semanas"] == 8
        assert ruta["horas_por_semana"] == 4
    
    def test_obtener_ruta_estructurada_intermedio(self, generador):
        """Verifica ruta estructurada de nivel intermedio."""
        ruta = generador.obtener_ruta_estructurada("intermedio")
        
        assert "error" not in ruta
        assert "semanas" in ruta
        assert ruta["nivel"] == "intermedio"
    
    def test_obtener_ruta_estructurada_avanzado(self, generador):
        """Verifica ruta estructurada de nivel avanzado."""
        ruta = generador.obtener_ruta_estructurada("avanzado")
        
        assert "error" not in ruta
        assert "semanas" in ruta
        assert ruta["nivel"] == "avanzado"
    
    def test_obtener_ruta_estructurada_inexistente(self, generador):
        """Verifica manejo de nivel inexistente."""
        ruta = generador.obtener_ruta_estructurada("inexistente")
        
        assert "error" in ruta
        assert "rutas_disponibles" in ruta
    
    def test_listar_rutas_disponibles(self, generador):
        """Verifica listado de rutas disponibles."""
        rutas = generador.listar_rutas_disponibles()
        
        assert len(rutas) == 3
        niveles = [r["nivel"] for r in rutas]
        assert "principiante" in niveles
        assert "intermedio" in niveles
        assert "avanzado" in niveles
    
    def test_generar_ruta_por_perfil_existente(self, generador):
        """Verifica generación de ruta para perfil existente."""
        ruta = generador.generar_ruta_por_perfil("cloud_engineer", horas_por_semana=4)
        
        assert "error" not in ruta
        assert "perfil" in ruta
        assert "ruta" in ruta
        assert "duracion_estimada_semanas" in ruta
    
    def test_generar_ruta_por_perfil_inexistente(self, generador):
        """Verifica manejo de perfil inexistente."""
        ruta = generador.generar_ruta_por_perfil("perfil_inexistente")
        
        assert "error" in ruta
        assert "perfiles_disponibles" in ruta
    
    def test_generar_ruta_con_cursos_completados(self, generador):
        """Verifica que excluye cursos ya completados."""
        ruta_sin_completados = generador.generar_ruta_por_perfil(
            "cloud_engineer",
            cursos_completados=[]
        )
        
        ruta_con_completados = generador.generar_ruta_por_perfil(
            "cloud_engineer",
            cursos_completados=["gcp-001", "gcp-002"]
        )
        
        assert ruta_con_completados["cursos_pendientes"] < ruta_sin_completados["cursos_pendientes"]
    
    def test_generar_ruta_por_habilidades(self, generador):
        """Verifica generación de ruta por habilidades."""
        ruta = generador.generar_ruta_por_habilidades(
            habilidades_objetivo=["VPC", "IAM"],
            horas_por_semana=4
        )
        
        assert "error" not in ruta
        assert "habilidades_objetivo" in ruta
        assert "ruta" in ruta
    
    def test_generar_ruta_por_habilidades_inexistentes(self, generador):
        """Verifica manejo de habilidades no encontradas."""
        ruta = generador.generar_ruta_por_habilidades(
            habilidades_objetivo=["habilidad_inexistente_xyz"],
            horas_por_semana=4
        )
        
        assert "error" in ruta
    
    def test_generar_ruta_rapida(self, generador):
        """Verifica generación de ruta rápida."""
        ruta = generador.generar_ruta_rapida(
            categoria_id="google_cloud",
            horas_disponibles=10,
            nivel="principiante"
        )
        
        assert "error" not in ruta
        assert "cursos_seleccionados" in ruta
        assert ruta["horas_utilizadas"] <= 10
    
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
        # gcp-002 depende de gcp-001
        cursos = ["gcp-002", "gcp-001"]
        ordenados = generador._ordenar_por_dependencias(cursos)
        
        # gcp-001 debe aparecer antes que gcp-002
        assert ordenados.index("gcp-001") < ordenados.index("gcp-002")
    
    def test_horas_semanales_afectan_duracion(self, generador):
        """Verifica que más horas semanales reducen la duración."""
        ruta_2h = generador.generar_ruta_por_perfil("cloud_engineer", horas_por_semana=2)
        ruta_8h = generador.generar_ruta_por_perfil("cloud_engineer", horas_por_semana=8)
        
        assert ruta_2h["duracion_estimada_semanas"] >= ruta_8h["duracion_estimada_semanas"]
    
    def test_ruta_estructurada_con_semanas_completadas(self, generador):
        """Verifica progreso en ruta estructurada."""
        ruta = generador.obtener_ruta_estructurada(
            nivel="principiante",
            semanas_completadas=[1, 2, 3]
        )
        
        assert ruta["semanas_completadas"] == 3
        assert ruta["progreso_porcentaje"] == 37.5  # 3/8 * 100


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
