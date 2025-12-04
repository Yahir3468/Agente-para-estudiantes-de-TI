# 🎓 Agente para Estudiantes de TI

Un agente inteligente diseñado para ayudar a estudiantes de Tecnologías de la Información a crear rutas de aprendizaje personalizadas enfocadas en **Google Cloud Platform** y resolver dudas de manera rápida y eficiente.

## 🎯 Objetivo

Este agente está diseñado especialmente para **estudiantes que trabajan y tienen poco tiempo** para estudiar. Ofrece:

- **Rutas de aprendizaje estructuradas de 8 semanas** por nivel (Principiante, Intermedio, Avanzado)
- **Formato micro-learning**: Actividades de 20-30 minutos
- **4 horas por semana** de estudio recomendado
- **Énfasis en nube, infraestructura, datos, automatización** y habilidades profesionales
- **Resolución de dudas** sobre temas técnicos de Google Cloud

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

### Uso programático

```python
from src.agente import AgenteEstudiantes

# Crear instancia del agente
agente = AgenteEstudiantes()

# Configurar perfil (4 horas semanales recomendado)
agente.configurar_perfil(
    nombre="María",
    horas_disponibles_semana=4,
    objetivo_carrera="cloud_engineer",
    nivel_experiencia="principiante"
)

# Obtener ruta estructurada de 8 semanas
ruta = agente.obtener_ruta_estructurada(nivel="principiante")
for semana in ruta["semanas"]:
    print(f"Semana {semana['semana']}: {semana['titulo']}")
    print(f"  Mini-ejercicio: {semana['mini_ejercicio']}")

# Marcar semana como completada
agente.marcar_semana_completada(1)

# Resolver una duda
respuesta = agente.resolver_duda("¿Qué es una VPC en Google Cloud?")
print(respuesta)

# Ver progreso
progreso = agente.obtener_progreso()
print(f"Progreso: {progreso['ruta_actual']['porcentaje']}%")
```

## 📚 Rutas de Aprendizaje (8 Semanas)

### ✅ Ruta Principiante
**Objetivo:** Desarrollar fundamentos sólidos en computación en la nube, habilidades digitales y lógica técnica.

| Semana | Tema | Curso | Mini-Ejercicio |
|--------|------|-------|----------------|
| 1 | Fundamentos Digitales | Digital Productivity | Crear calendario de estudio |
| 2 | Introducción a Google Cloud | GCP Core Infrastructure | Dibujar arquitectura básica |
| 3 | Computación y Almacenamiento | Compute Engine | Comparar tipos de VM |
| 4 | Redes Básicas | Networking Fundamentals | VPC vs red local |
| 5 | Seguridad Básica | Security for Beginners | Política IAM |
| 6 | Bases de Datos | Introduction to SQL | Crear tabla SQL |
| 7 | Automatización | Scripting Bash/Python | Script básico |
| 8 | **Proyecto Final** | - | VM + Firewall + Bucket |

### ✅ Ruta Intermedio
**Objetivo:** Fortalecer infraestructura, redes, seguridad y operaciones en Google Cloud.

| Semana | Tema | Curso | Mini-Ejercicio |
|--------|------|-------|----------------|
| 1 | Infraestructura Avanzada | Compute Engine Deep Dive | Justificar tipos de máquina |
| 2 | Redes Avanzadas | Networking Advanced | Diagrama red híbrida |
| 3 | Seguridad y Cumplimiento | IAM Best Practices | Políticas por rol |
| 4 | Contenedores | Kubernetes on GCP | Componentes de cluster |
| 5 | Infraestructura como Código | Terraform Basics | Archivo Terraform |
| 6 | Observabilidad | Monitoring & Logging | Dashboard métricas |
| 7 | Bases de Datos Cloud | Cloud SQL & Firestore | SQL vs NoSQL |
| 8 | **Proyecto Final** | - | Arquitectura completa |

### ✅ Ruta Avanzado
**Objetivo:** Especialización en arquitectura cloud, datos, automatización y soluciones escalables.

| Semana | Tema | Curso | Mini-Ejercicio |
|--------|------|-------|----------------|
| 1 | Arquitectura Escalable | Architecting with GCE | Diseño 10K usuarios |
| 2 | Kubernetes Profesional | GKE Architecture | Namespaces y políticas |
| 3 | Serverless | Cloud Functions/Run | Pipeline CI/CD |
| 4 | Data Engineering | Data Engineering GCP | Flujo ETL |
| 5 | Machine Learning | Vertex AI | Modelo AutoML |
| 6 | Seguridad Avanzada | Security Engineering | Reglas multi-nivel |
| 7 | Optimización de Costos | Cost Management | Plan reducción 20-30% |
| 8 | **Proyecto Final** | - | Solución empresarial |

## 👔 Perfiles de Carrera

- **Cloud Engineer** - Diseña y gestiona infraestructura en Google Cloud
- **Cloud Architect** - Diseña soluciones empresariales escalables
- **Data Engineer** - Diseña y gestiona pipelines de datos
- **DevOps Engineer** - Automatiza operaciones de desarrollo
- **Security Engineer** - Implementa seguridad en entornos cloud

## 💡 Características para Estudiantes que Trabajan

### Formato Micro-Learning
- **Sesiones de 20-30 minutos** que se adaptan a tu agenda
- **4 horas por semana** de estudio estructurado
- **Mini-ejercicios prácticos** en cada semana

### Progreso Medible
- Marca semanas completadas
- Visualiza tu porcentaje de avance
- Proyectos finales para cada nivel

### Tips de Estudio Incluidos
- Técnica Pomodoro
- Micro-learning (20-30 min)
- Práctica activa con ejercicios
- Documentación del aprendizaje
- Aprovechamiento de tiempos muertos

## 📁 Estructura del Proyecto

```
Agente-para-estudiantes-de-TI/
├── data/
│   ├── cursos.json          # Matriz de cursos con rutas de 8 semanas
│   └── base_conocimiento.json # Base de conocimiento para dudas
├── src/
│   ├── __init__.py
│   ├── agente.py            # Agente principal
│   ├── generador_rutas.py   # Generador de rutas estructuradas
│   ├── asistente_dudas.py   # Asistente de resolución de dudas
│   ├── data_loader.py       # Carga de datos
│   └── cli.py               # Interfaz de línea de comandos
├── tests/                   # 58 pruebas unitarias
├── main.py                  # Punto de entrada
├── pyproject.toml           # Configuración del proyecto
└── README.md
```

## 🧪 Pruebas

```bash
# Ejecutar todas las pruebas (58 tests)
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

Este proyecto fue creado pensando en todos los estudiantes de TI que trabajan y buscan maneras eficientes de seguir aprendiendo y creciendo profesionalmente en el mundo cloud.
