# 🟡 Ruta Intermedio (8 semanas)

**Objetivo:** Fortalecer infraestructura, redes, seguridad y operaciones en Google Cloud. Ideal para alumnos que ya manejan conceptos básicos.

**Dedicación semanal:** 4 horas  
**Formato:** Micro-learning (20-30 min por actividad)  
**Prerequisito:** Completar la Ruta Principiante o tener conocimientos equivalentes

---

## Semana 1 — Infraestructura Avanzada

### Curso
**Google Cloud Compute Engine Deep Dive**  
⏱️ Duración sugerida: 3-4 horas

### Temas
- Tipos de máquinas personalizadas
- Instancias preemptibles y spot
- Grupos de instancias
- Plantillas de instancias

### Mini-reto
📝 Elegir 3 tipos de máquina y justificar su uso:

| Tipo de Máquina | Caso de Uso | Justificación |
|-----------------|-------------|---------------|
| | | |
| | | |
| | | |

---

## Semana 2 — Redes Avanzadas

### Curso
**Networking in Google Cloud: Advanced**  
⏱️ Duración sugerida: 3-4 horas

### Temas
- VPN (Virtual Private Network)
- Cloud Router
- VPC Peering
- Cloud NAT

### Reto
📝 Crear diagrama de red híbrida que incluya:
- Red on-premises conectada a GCP
- VPN Site-to-Site
- Cloud Router para enrutamiento dinámico
- Subnets en diferentes regiones

```
┌─────────────────┐         ┌─────────────────┐
│   On-Premises   │   VPN   │   Google Cloud  │
│    Network      │◄───────►│      VPC        │
│   10.0.0.0/16   │         │   10.1.0.0/16   │
└─────────────────┘         └─────────────────┘
```

---

## Semana 3 — Seguridad y Cumplimiento

### Curso
**Cloud IAM & Security Best Practices**  
⏱️ Duración sugerida: 3-4 horas

### Temas
- Políticas de organización
- Service Accounts
- Auditoría y cumplimiento
- Secret Manager

### Reto
📝 Crear política de acceso por rol:

**Admin:**
```yaml
roles:
  - roles/owner
  - roles/iam.securityAdmin
recursos:
  - Todos los proyectos
```

**Developer:**
```yaml
roles:
  - roles/compute.developer
  - roles/storage.objectViewer
  - roles/cloudsql.client
recursos:
  - Proyectos de desarrollo
```

**Operador:**
```yaml
roles:
  - roles/monitoring.viewer
  - roles/logging.viewer
  - roles/compute.viewer
recursos:
  - Proyectos de producción (solo lectura)
```

---

## Semana 4 — Contenedores

### Curso
**Introduction to Kubernetes on Google Cloud**  
⏱️ Duración sugerida: 3-4 horas

### Temas
- Conceptos de contenedores
- Docker fundamentals
- Kubernetes architecture
- Google Kubernetes Engine (GKE)

### Reto
📝 Describir los componentes de un cluster:

| Componente | Descripción | Función |
|------------|-------------|---------|
| **Pod** | | |
| **Node** | | |
| **Namespace** | | |
| **Deployment** | | |
| **Service** | | |
| **ConfigMap** | | |

---

## Semana 5 — Automatización e Infraestructura como Código

### Curso
**Google Cloud Deployment Manager / Terraform Basics**  
⏱️ Duración sugerida: 3-4 horas

### Temas
- Infraestructura como Código (IaC)
- Terraform básico
- Deployment Manager
- Gestión de estado

### Reto
📝 Crear archivo de Terraform para una VM:

```hcl
# main.tf
provider "google" {
  project = "mi-proyecto"
  region  = "us-central1"
}

resource "google_compute_instance" "vm_instance" {
  name         = "mi-vm"
  machine_type = "e2-medium"
  zone         = "us-central1-a"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }

  network_interface {
    network = "default"
    access_config {
      # Ephemeral public IP
    }
  }

  # Agregar tags, labels y metadata
}
```

---

## Semana 6 — Observabilidad

### Curso
**Monitoring, Logging, and Error Reporting**  
⏱️ Duración sugerida: 3-4 horas

### Temas
- Cloud Monitoring
- Cloud Logging
- Error Reporting
- Uptime Checks
- Alertas

### Reto
📝 Plantear un dashboard con 4 métricas críticas:

| Métrica | Tipo | Umbral Alerta | Importancia |
|---------|------|---------------|-------------|
| CPU Usage | Gauge | > 80% | Alta |
| Memory Usage | Gauge | > 85% | Alta |
| Request Latency | Histogram | > 500ms | Media |
| Error Rate | Counter | > 5% | Crítica |

**Dashboard propuesto:**
```
┌─────────────────────────────────────────────┐
│           Dashboard de Aplicación           │
├──────────────────┬──────────────────────────┤
│   CPU Usage      │    Memory Usage          │
│   [Graph]        │    [Graph]               │
├──────────────────┼──────────────────────────┤
│ Request Latency  │    Error Rate            │
│   [Graph]        │    [Graph]               │
└──────────────────┴──────────────────────────┘
```

---

## Semana 7 — Bases de Datos en la Nube

### Curso
**Cloud SQL y Firestore Fundamentals**  
⏱️ Duración sugerida: 3-4 horas

### Temas
- Cloud SQL (MySQL, PostgreSQL, SQL Server)
- Cloud Spanner
- Firestore (NoSQL)
- Bigtable

### Reto
📝 Comparar SQL vs NoSQL - ¿cuándo usar qué?

| Criterio | SQL (Cloud SQL) | NoSQL (Firestore) |
|----------|-----------------|-------------------|
| Estructura de datos | Esquema fijo | Esquema flexible |
| Escalabilidad | Vertical | Horizontal |
| Transacciones | ACID completo | Limitado |
| Consultas complejas | Excelente | Limitado |
| Casos de uso | | |

**Decisión:**
- Usar **SQL** cuando: _________________________________
- Usar **NoSQL** cuando: _______________________________

---

## Semana 8 — Proyecto Final Intermedio

### Actividad
Construir una arquitectura pequeña pero realista que incluya:

- ✅ VM backend con aplicación
- ✅ Base de datos Cloud SQL
- ✅ Balanceador de carga
- ✅ Log monitoring configurado

### Arquitectura propuesta

```
                    ┌─────────────────┐
                    │  Load Balancer  │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
        ┌─────▼─────┐  ┌─────▼─────┐  ┌─────▼─────┐
        │   VM 1    │  │   VM 2    │  │   VM 3    │
        │ (Backend) │  │ (Backend) │  │ (Backend) │
        └─────┬─────┘  └─────┬─────┘  └─────┬─────┘
              │              │              │
              └──────────────┼──────────────┘
                             │
                    ┌────────▼────────┐
                    │   Cloud SQL     │
                    │  (PostgreSQL)   │
                    └─────────────────┘
                             │
                    ┌────────▼────────┐
                    │ Cloud Logging   │
                    │ & Monitoring    │
                    └─────────────────┘
```

### Entregables

1. **Diagrama de arquitectura** completo y detallado

2. **Checklist de seguridad:**

| Verificación | Estado |
|--------------|--------|
| Firewall configurado con reglas mínimas | ⬜ |
| Cloud SQL sin IP pública | ⬜ |
| Service Account con permisos mínimos | ⬜ |
| Logs de auditoría habilitados | ⬜ |
| Backups automáticos configurados | ⬜ |
| SSL/TLS en todas las conexiones | ⬜ |

### Criterios de evaluación

| Criterio | Puntos |
|----------|--------|
| Arquitectura funcional | 25 |
| Seguridad implementada | 25 |
| Monitoreo configurado | 25 |
| Documentación técnica | 25 |

---

## 📊 Resumen del Progreso

| Semana | Tema | Estado |
|--------|------|--------|
| 1 | Infraestructura Avanzada | ⬜ |
| 2 | Redes Avanzadas | ⬜ |
| 3 | Seguridad y Cumplimiento | ⬜ |
| 4 | Contenedores | ⬜ |
| 5 | Automatización e IaC | ⬜ |
| 6 | Observabilidad | ⬜ |
| 7 | Bases de Datos en la Nube | ⬜ |
| 8 | Proyecto Final | ⬜ |

---

## 🔗 Recursos Adicionales

- [Terraform Google Provider Docs](https://registry.terraform.io/providers/hashicorp/google/latest/docs)
- [Kubernetes Documentation](https://kubernetes.io/docs/home/)
- [Cloud SQL Best Practices](https://cloud.google.com/sql/docs/mysql/best-practices)

---

[← Ruta Principiante](principiante.md) | [Volver al inicio](../README.md) | [Ruta Avanzado →](avanzado.md)
