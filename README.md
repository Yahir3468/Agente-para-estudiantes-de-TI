# 🎓 Agente para Estudiantes de TI

Un agente inteligente diseñado para ayudar a estudiantes de Tecnologías de la Información a crear rutas de aprendizaje personalizadas y resolver dudas de manera rápida y eficiente.

## 🎯 Objetivo

Este agente está diseñado especialmente para **estudiantes que trabajan y tienen poco tiempo** para estudiar. Ofrece:

- **Rutas de aprendizaje personalizadas** basadas en tu perfil de carrera objetivo
- **Cursos autogestivos** organizados por categoría y nivel
- **Resolución de dudas** sobre temas técnicos comunes
- **Optimización del tiempo de estudio** con tips y técnicas de aprendizaje ágil

## 🚀 Instalación

### Requisitos
- Python 3.8 o superior

### Instalación básica

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/Agente-para-estudiantes-de-TI.git
cd Agente-para-estudiantes-de-TI

# Ejecutar el agente
python main.py
```

### Instalación para desarrollo

```bash
# Instalar dependencias de desarrollo
pip install -e ".[dev]"

# Ejecutar pruebas
pytest
```

## 📖 Uso

### Interfaz de línea de comandos (CLI)

```bash
python main.py
```

Esto abrirá un menú interactivo con las siguientes opciones:

1. **Configurar mi perfil** - Define tu nombre, tiempo disponible y objetivo de carrera
2. **Ver rutas de aprendizaje** - Explora los perfiles de carrera disponibles
3. **Generar ruta personalizada** - Crea tu ruta por perfil o habilidades específicas
4. **Ruta rápida** - Para cuando tienes muy poco tiempo
5. **Resolver una duda** - Busca respuestas a preguntas técnicas
6. **Ver mi progreso** - Monitorea tu avance
7. **Marcar curso completado** - Registra los cursos terminados
8. **Tips de estudio** - Técnicas para aprender de manera eficiente
9. **Ver categorías y cursos** - Lista todos los cursos disponibles

### Uso programático

```python
from src.agente import AgenteEstudiantes

# Crear instancia del agente
agente = AgenteEstudiantes()

# Configurar perfil
agente.configurar_perfil(
    nombre="Juan",
    horas_disponibles_semana=8,
    objetivo_carrera="desarrollador_web",
    nivel_experiencia="principiante"
)

# Obtener ruta de aprendizaje
ruta = agente.obtener_ruta_aprendizaje()
print(ruta)

# Resolver una duda
respuesta = agente.resolver_duda("¿Qué es una variable en Python?")
print(respuesta)

# Generar ruta rápida (cuando tienes poco tiempo)
ruta_rapida = agente.obtener_ruta_rapida(
    categoria="programacion",
    horas_disponibles=15,
    nivel_maximo="basico"
)
print(ruta_rapida)
```

## 📚 Categorías de Cursos

| Categoría | Descripción |
|-----------|-------------|
| **Programación** | Python, JavaScript, Flask, React |
| **Bases de Datos** | SQL, MySQL, MongoDB |
| **Redes** | Fundamentos, Cisco, Seguridad en redes |
| **Ciberseguridad** | Ethical Hacking, Análisis de malware |
| **Cloud** | AWS, Docker, Kubernetes |
| **Ciencia de Datos** | Análisis de datos, Machine Learning |

## 👔 Perfiles de Carrera

- **Desarrollador Web Full Stack** - Frontend y Backend
- **Administrador de Redes** - Infraestructura y comunicaciones
- **Científico de Datos** - Análisis y machine learning
- **Especialista en Ciberseguridad** - Seguridad informática
- **Ingeniero Cloud** - Infraestructura en la nube
- **Administrador de Bases de Datos** - Gestión de datos

## 💡 Características para Estudiantes que Trabajan

### Microaprendizaje
Si tienes menos de 5 horas semanales, el agente te sugiere:
- Sesiones de 30 minutos máximo
- Técnica Pomodoro (25 min estudio + 5 min descanso)
- Contenido en pequeñas porciones

### Rutas Rápidas
Para aprender lo esencial en poco tiempo:
- Selecciona una categoría
- Indica las horas totales disponibles
- Obtén los cursos esenciales que caben en ese tiempo

### Tips de Estudio Incluidos
- Técnica Pomodoro
- Práctica activa
- Espaciado de repetición
- Microaprendizaje
- Enseñar para aprender

## 📁 Estructura del Proyecto

```
Agente-para-estudiantes-de-TI/
├── data/
│   ├── cursos.json          # Matriz de cursos autogestivos
│   └── base_conocimiento.json # Base de conocimiento para dudas
├── src/
│   ├── __init__.py
│   ├── agente.py            # Agente principal
│   ├── generador_rutas.py   # Generador de rutas de aprendizaje
│   ├── asistente_dudas.py   # Asistente de resolución de dudas
│   ├── data_loader.py       # Carga de datos
│   └── cli.py               # Interfaz de línea de comandos
├── tests/
│   ├── test_agente.py
│   ├── test_generador_rutas.py
│   ├── test_asistente_dudas.py
│   └── test_data_loader.py
├── main.py                  # Punto de entrada
├── pyproject.toml           # Configuración del proyecto
└── README.md
```

## 🧪 Pruebas

```bash
# Ejecutar todas las pruebas
pytest

# Ejecutar con cobertura
pytest --cov=src

# Ejecutar pruebas específicas
pytest tests/test_agente.py -v
```

## 🤝 Contribuir

Las contribuciones son bienvenidas. Para contribuir:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 🙏 Agradecimientos

Este proyecto fue creado pensando en todos los estudiantes de TI que trabajan y buscan maneras eficientes de seguir aprendiendo y creciendo profesionalmente.
