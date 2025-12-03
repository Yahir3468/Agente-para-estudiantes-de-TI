# 🎓 Agente de Aprendizaje para Estudiantes de TI

Un agente inteligente diseñado especialmente para estudiantes de Tecnologías de la Información que trabajan y tienen poco tiempo para estudiar.

## 🎯 Objetivo

Este agente ayuda a los estudiantes de TI a:
- **Crear rutas de aprendizaje personalizadas** basadas en sus objetivos y tiempo disponible
- **Acceder a cursos autogestivos** organizados en una matriz estructurada
- **Resolver dudas** sobre temas de TI de manera rápida
- **Optimizar su tiempo de estudio** con consejos prácticos

## 🚀 Características

- ✅ Rutas de aprendizaje predefinidas para diferentes perfiles (Frontend, Backend, DevOps, etc.)
- ✅ Generación de rutas personalizadas según habilidades objetivo
- ✅ Catálogo de cursos autogestivos organizados por categoría y nivel
- ✅ Sistema de prerequisitos para aprendizaje estructurado
- ✅ Cálculo de tiempo estimado basado en disponibilidad del estudiante
- ✅ Tips de estudio para estudiantes que trabajan

## 📁 Estructura del Proyecto

```
├── src/
│   ├── __init__.py        # Módulo principal
│   ├── agente.py          # Lógica del agente de aprendizaje
│   └── interfaz.py        # Interfaz interactiva de línea de comandos
├── data/
│   └── cursos.json        # Matriz de cursos autogestivos
├── requirements.txt       # Dependencias del proyecto
└── README.md
```

## 💻 Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/Yahir3468/Agente-para-estudiantes-de-TI.git
cd Agente-para-estudiantes-de-TI
```

2. (Opcional) Crea un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## 🎮 Uso

### Interfaz Interactiva

Ejecuta la interfaz interactiva para explorar todas las funcionalidades:

```bash
cd src
python interfaz.py
```

### Uso Programático

```python
from src.agente import AgenteEstudianteTI

# Crear instancia del agente
agente = AgenteEstudianteTI()

# Ver rutas predefinidas
rutas = agente.listar_rutas_predefinidas()
for ruta in rutas:
    print(f"- {ruta['nombre']}: {ruta['duracion_total_horas']}h")

# Crear ruta personalizada
ruta_personal = agente.generar_ruta_personalizada(
    habilidades_objetivo=["Python", "APIs", "SQL"],
    horas_disponibles_semana=5,
    nivel_actual="principiante"
)

print(f"Cursos en tu ruta: {len(ruta_personal['cursos'])}")
print(f"Tiempo estimado: {ruta_personal['semanas_estimadas']} semanas")

# Buscar cursos por habilidad
cursos_python = agente.buscar_cursos_por_habilidad("Python")

# Resolver dudas sobre un tema
resultado = agente.responder_duda("programación orientada a objetos")
```

### Demostración Rápida

```bash
cd src
python agente.py
```

## 📚 Catálogo de Cursos

El agente incluye cursos en las siguientes categorías:

| Categoría | Cursos Disponibles |
|-----------|-------------------|
| Programación | Python Básico, Python Intermedio |
| Desarrollo Web | HTML/CSS, JavaScript, React |
| Bases de Datos | SQL Básico |
| DevOps | Docker, Git/GitHub |
| Cloud | Introducción a AWS |
| Sistemas Operativos | Linux Básico |
| Redes | Redes Básico |
| Ciberseguridad | Introducción a Ciberseguridad |
| IA/ML | Introducción a IA |
| Backend | Diseño de APIs REST |
| Metodologías | Scrum Básico |

## 🛤️ Rutas Predefinidas

1. **Desarrollador Web Frontend** - HTML, CSS, JavaScript, React (40h)
2. **Desarrollador Backend Python** - Python, SQL, APIs (48h)
3. **DevOps Básico** - Linux, Git, Docker, AWS (33h)
4. **Ciberseguridad Inicial** - Redes, Linux, Seguridad (28h)
5. **Data Science Intro** - Python, SQL, IA/ML (48h)

## 💡 Para Estudiantes que Trabajan

El agente está optimizado para estudiantes con poco tiempo:

- 📊 **Calcula el tiempo real** basado en tus horas disponibles por semana
- 💡 **Proporciona tips de estudio** adaptados a tu disponibilidad
- ⚡ **Prioriza la práctica** sobre la teoría cuando hay poco tiempo
- 📱 **Sugiere aprovechar tiempos muertos** para repaso

## 🤝 Contribuir

¿Quieres agregar más cursos o mejorar el agente?

1. Agrega cursos en `data/cursos.json`
2. Sigue la estructura existente de los cursos
3. Asegúrate de incluir prerequisitos si aplican

## 📄 Licencia

Este proyecto está disponible para uso educativo.

---

**¡Éxito en tu aprendizaje! 🚀**
