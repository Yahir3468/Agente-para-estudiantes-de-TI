# 🟢 Ruta Principiante (8 semanas)

**Objetivo:** Desarrollar fundamentos sólidos en computación en la nube, habilidades digitales y lógica técnica para cualquier área de TI.

**Dedicación semanal:** 4 horas  
**Formato:** Micro-learning (20-30 min por actividad)

---

## Semana 1 — Fundamentos Digitales

### Curso
**Digital Productivity**  
⏱️ Duración sugerida: 2 horas

### Actividad
- Gestión de archivos
- Correo electrónico
- Calendarios
- Herramientas de colaboración

### Mini-ejercicio
📝 Crear un calendario semanal de estudio en Google Calendar con:
- Bloques de tiempo para cada módulo del curso
- Recordatorios para las actividades
- Código de colores para diferentes tipos de tareas

---

## Semana 2 — Introducción a Google Cloud

### Curso
**Google Cloud Fundamentals: Core Infrastructure**  
⏱️ Duración sugerida: 3 horas

### Actividad
- Conceptos de nube
- Regiones y zonas
- Máquinas virtuales
- Almacenamiento

### Mini-ejercicio
📝 Dibujar arquitectura básica de una aplicación monolítica que incluya:
- Servidor web
- Base de datos
- Almacenamiento de archivos
- Conexión a internet

---

## Semana 3 — Computación y Almacenamiento

### Curso
**Compute Engine: Getting Started**  
⏱️ Duración: 3 horas

### Actividad
- Crear y configurar una máquina virtual en consola (simulada)
- Entender tipos de instancias
- Configurar discos persistentes

### Mini-ejercicio
📝 Comparar tipos de VM:
| Tipo de VM | Uso recomendado | vCPUs | Memoria |
|------------|-----------------|-------|---------|
| e2-micro | | | |
| e2-small | | | |
| n1-standard-1 | | | |
| n2-highmem-2 | | | |

---

## Semana 4 — Redes Básicas en la Nube

### Curso
**Networking in Google Cloud: Fundamentals**  
⏱️ Duración: 3 horas

### Actividad
- Redes VPC (Virtual Private Cloud)
- Subnets
- Reglas básicas de firewall

### Mini-ejercicio
📝 Identificar diferencias entre VPC y red local:
| Característica | VPC en Cloud | Red Local |
|---------------|--------------|-----------|
| Escalabilidad | | |
| Costo inicial | | |
| Mantenimiento | | |
| Seguridad | | |

---

## Semana 5 — Seguridad Básica

### Curso
**Security in Google Cloud for Beginners**  
⏱️ Duración: 2-3 horas

### Actividad
- IAM (Identity and Access Management)
- Roles y permisos
- Principio de mínimo privilegio

### Mini-ejercicio
📝 Crear política de acceso para perfil "estudiante":
```
Rol: Estudiante Cloud
Permisos:
- compute.instances.list (Ver VMs)
- storage.objects.get (Leer objetos)
- ...

Recursos permitidos:
- Proyecto: proyecto-educativo
- ...
```

---

## Semana 6 — Introducción a Bases de Datos

### Curso
**Introduction to SQL**  
⏱️ Duración: 2-3 horas

### Actividad
- Comandos básicos: SELECT, INSERT, UPDATE, DELETE
- Creación de tablas
- Consultas simples

### Mini-ejercicio
📝 Crear tabla "estudiantes" con 5 registros:
```sql
CREATE TABLE estudiantes (
    id INT PRIMARY KEY,
    nombre VARCHAR(100),
    email VARCHAR(100),
    carrera VARCHAR(50),
    semestre INT
);

INSERT INTO estudiantes VALUES
    (1, 'Ana García', 'ana@email.com', 'Ing. Sistemas', 3),
    -- Agregar 4 registros más
;
```

---

## Semana 7 — Automatización Básica

### Curso
**Introduction to Scripting (Bash/Python)**  
⏱️ Duración: 3 horas

### Actividad
- Conceptos básicos de scripting
- Variables y estructuras de control
- Automatización de tareas simples

### Mini-ejercicio
📝 Script que imprime fecha/hora y crea carpeta:

**Bash:**
```bash
#!/bin/bash
echo "Fecha y hora actual: $(date)"
mkdir -p ~/backup_$(date +%Y%m%d)
echo "Carpeta de backup creada"
```

**Python:**
```python
import os
from datetime import datetime

print(f"Fecha y hora actual: {datetime.now()}")
folder_name = f"backup_{datetime.now().strftime('%Y%m%d')}"
os.makedirs(folder_name, exist_ok=True)
print("Carpeta de backup creada")
```

---

## Semana 8 — Proyecto Final

### Actividad
Crear un entorno simple en GCP que incluya:
- ✅ Una máquina virtual (VM)
- ✅ Reglas de firewall configuradas
- ✅ Un bucket de almacenamiento (Cloud Storage)

### Entregables

1. **Capturas de pantalla** de:
   - Consola de GCP con la VM creada
   - Configuración de firewall
   - Bucket de almacenamiento

2. **Documento explicativo** (5 minutos de lectura):
   - Descripción de cada componente
   - Configuraciones aplicadas
   - Justificación de decisiones técnicas
   - Posibles mejoras

### Criterios de evaluación
| Criterio | Puntos |
|----------|--------|
| VM correctamente configurada | 25 |
| Firewall con reglas apropiadas | 25 |
| Bucket creado y accesible | 25 |
| Documentación clara y completa | 25 |

---

## 📊 Resumen del Progreso

| Semana | Tema | Estado |
|--------|------|--------|
| 1 | Fundamentos Digitales | ⬜ |
| 2 | Introducción a Google Cloud | ⬜ |
| 3 | Computación y Almacenamiento | ⬜ |
| 4 | Redes Básicas | ⬜ |
| 5 | Seguridad Básica | ⬜ |
| 6 | Bases de Datos | ⬜ |
| 7 | Automatización | ⬜ |
| 8 | Proyecto Final | ⬜ |

---

## 🔗 Recursos Adicionales

- [Documentación de Google Cloud](https://cloud.google.com/docs)
- [Google Cloud Skills Boost](https://www.cloudskillsboost.google/)
- [Qwiklabs - Labs prácticos](https://www.qwiklabs.com/)

---

[← Volver al inicio](../README.md) | [Siguiente: Ruta Intermedio →](intermedio.md)
