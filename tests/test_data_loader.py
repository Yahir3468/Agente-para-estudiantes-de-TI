"""
Pruebas unitarias para el módulo data_loader.
"""

import pytest
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import data_loader


class TestDataLoader:
    """Pruebas para las funciones de carga de datos."""
    
    def test_cargar_cursos(self):
        """Verifica que se cargan los cursos correctamente."""
        datos = data_loader.cargar_cursos()
        
        assert "categorias" in datos
        assert "perfiles_carrera" in datos
        assert "rutas_aprendizaje" in datos
        assert len(datos["categorias"]) > 0
        assert len(datos["perfiles_carrera"]) > 0
    
    def test_cargar_base_conocimiento(self):
        """Verifica que se carga la base de conocimiento correctamente."""
        datos = data_loader.cargar_base_conocimiento()
        
        assert "temas" in datos
        assert "tips_estudio" in datos
        assert len(datos["tips_estudio"]) > 0
    
    def test_obtener_curso_por_id_existente(self):
        """Verifica que se obtiene un curso existente por ID."""
        curso = data_loader.obtener_curso_por_id("gcp-001")
        
        assert curso is not None
        assert curso["id"] == "gcp-001"
        assert "nombre" in curso
        assert "categoria" in curso
    
    def test_obtener_curso_por_id_inexistente(self):
        """Verifica que retorna None para curso inexistente."""
        curso = data_loader.obtener_curso_por_id("inexistente-999")
        
        assert curso is None
    
    def test_obtener_cursos_por_categoria(self):
        """Verifica que se obtienen cursos por categoría."""
        cursos = data_loader.obtener_cursos_por_categoria("google_cloud")
        
        assert len(cursos) > 0
        assert all("id" in c for c in cursos)
        assert all("nombre" in c for c in cursos)
    
    def test_obtener_cursos_por_categoria_inexistente(self):
        """Verifica que retorna lista vacía para categoría inexistente."""
        cursos = data_loader.obtener_cursos_por_categoria("inexistente")
        
        assert cursos == []
    
    def test_obtener_cursos_por_nivel(self):
        """Verifica que se obtienen cursos por nivel."""
        cursos_principiante = data_loader.obtener_cursos_por_nivel("principiante")
        cursos_intermedios = data_loader.obtener_cursos_por_nivel("intermedio")
        cursos_avanzados = data_loader.obtener_cursos_por_nivel("avanzado")
        
        assert len(cursos_principiante) > 0
        assert all(c["nivel"] == "principiante" for c in cursos_principiante)
        
        assert len(cursos_intermedios) > 0
        assert all(c["nivel"] == "intermedio" for c in cursos_intermedios)
        
        assert len(cursos_avanzados) > 0
        assert all(c["nivel"] == "avanzado" for c in cursos_avanzados)
    
    def test_obtener_perfil_carrera_existente(self):
        """Verifica que se obtiene un perfil de carrera existente."""
        perfil = data_loader.obtener_perfil_carrera("cloud_engineer")
        
        assert perfil is not None
        assert perfil["id"] == "cloud_engineer"
        assert "nombre" in perfil
        assert "cursos_clave" in perfil
    
    def test_obtener_perfil_carrera_inexistente(self):
        """Verifica que retorna None para perfil inexistente."""
        perfil = data_loader.obtener_perfil_carrera("inexistente")
        
        assert perfil is None
    
    def test_listar_categorias(self):
        """Verifica que se listan las categorías correctamente."""
        categorias = data_loader.listar_categorias()
        
        assert len(categorias) > 0
        assert all("id" in c for c in categorias)
        assert all("nombre" in c for c in categorias)
        assert all("descripcion" in c for c in categorias)
    
    def test_listar_perfiles_carrera(self):
        """Verifica que se listan los perfiles de carrera."""
        perfiles = data_loader.listar_perfiles_carrera()
        
        assert len(perfiles) > 0
        assert all("id" in p for p in perfiles)
        assert all("nombre" in p for p in perfiles)
        assert all("descripcion" in p for p in perfiles)
    
    def test_obtener_ruta_aprendizaje(self):
        """Verifica que se obtiene una ruta de aprendizaje."""
        ruta = data_loader.obtener_ruta_aprendizaje("principiante")
        
        assert ruta is not None
        assert "semanas" in ruta
        assert len(ruta["semanas"]) == 8
    
    def test_listar_rutas_aprendizaje(self):
        """Verifica que se listan las rutas de aprendizaje."""
        rutas = data_loader.listar_rutas_aprendizaje()
        
        assert len(rutas) == 3  # principiante, intermedio, avanzado
        assert all("nivel" in r for r in rutas)
        assert all("duracion_semanas" in r for r in rutas)
    
    def test_obtener_configuracion(self):
        """Verifica que se obtiene la configuración."""
        config = data_loader.obtener_configuracion()
        
        assert "horas_por_semana" in config
        assert config["horas_por_semana"] == 4


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
