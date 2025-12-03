# 🔴 Ruta Avanzado (8 semanas)

**Objetivo:** Especialización en arquitectura en la nube, datos, automatización y soluciones cloud escalables.

**Dedicación semanal:** 4 horas  
**Formato:** Micro-learning (20-30 min por actividad)  
**Prerequisito:** Completar la Ruta Intermedio o tener experiencia equivalente

---

## Semana 1 — Arquitectura Escalable

### Curso
**Architecting with Google Compute Engine**  
⏱️ Duración sugerida: 3-4 horas

### Temas
- Diseño para alta disponibilidad
- Patrones de arquitectura cloud
- Auto-scaling
- Diseño multi-región

### Reto
📝 Diseñar arquitectura para 10,000 usuarios concurrentes:

**Requisitos:**
- Alta disponibilidad (99.9% uptime)
- Latencia < 200ms
- Escalamiento automático
- Recuperación ante desastres

**Arquitectura propuesta:**

```
                         ┌─────────────────────┐
                         │   Cloud CDN         │
                         │   (Cache global)    │
                         └──────────┬──────────┘
                                    │
                         ┌──────────▼──────────┐
                         │  Global Load        │
                         │  Balancer           │
                         └──────────┬──────────┘
                                    │
            ┌───────────────────────┼───────────────────────┐
            │                       │                       │
   ┌────────▼────────┐    ┌────────▼────────┐    ┌────────▼────────┐
   │ Region US-West  │    │ Region US-East  │    │ Region Europe   │
   │ ┌─────────────┐ │    │ ┌─────────────┐ │    │ ┌─────────────┐ │
   │ │ MIG (auto)  │ │    │ │ MIG (auto)  │ │    │ │ MIG (auto)  │ │
   │ │ 2-10 VMs    │ │    │ │ 2-10 VMs    │ │    │ │ 2-10 VMs    │ │
   │ └─────────────┘ │    │ └─────────────┘ │    │ └─────────────┘ │
   └────────┬────────┘    └────────┬────────┘    └────────┬────────┘
            │                      │                      │
            └──────────────────────┼──────────────────────┘
                                   │
                         ┌─────────▼─────────┐
                         │   Cloud Spanner   │
                         │   (Multi-region)  │
                         └───────────────────┘
```

**Justificación técnica:**
| Componente | Propósito | Capacidad |
|------------|-----------|-----------|
| Cloud CDN | | |
| Global LB | | |
| MIG (Managed Instance Groups) | | |
| Cloud Spanner | | |

---

## Semana 2 — Kubernetes Profesional

### Curso
**Architecting with Kubernetes on GKE**  
⏱️ Duración sugerida: 3-4 horas

### Temas
- GKE Autopilot vs Standard
- Helm Charts
- Service Mesh (Istio)
- GitOps con ArgoCD

### Reto
📝 Configurar namespaces y políticas de seguridad:

**Estructura de namespaces:**
```yaml
# namespaces.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: development
  labels:
    environment: dev
---
apiVersion: v1
kind: Namespace
metadata:
  name: staging
  labels:
    environment: staging
---
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    environment: prod
```

**Network Policy:**
```yaml
# network-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all-ingress
  namespace: production
spec:
  podSelector: {}
  policyTypes:
  - Ingress
  ingress: []
```

**Resource Quotas:**
```yaml
# resource-quota.yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: production-quota
  namespace: production
spec:
  hard:
    pods: "50"
    requests.cpu: "20"
    requests.memory: 40Gi
    limits.cpu: "40"
    limits.memory: 80Gi
```

---

## Semana 3 — Serverless y Microservicios

### Curso
**Developing Serverless Apps (Cloud Functions / Cloud Run)**  
⏱️ Duración sugerida: 3-4 horas

### Temas
- Cloud Functions (1st y 2nd gen)
- Cloud Run
- Eventarc
- Pub/Sub

### Reto
📝 Crear pipeline simple de CI/CD:

**cloudbuild.yaml:**
```yaml
steps:
  # Build
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/my-app:$COMMIT_SHA', '.']
  
  # Push to Container Registry
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/my-app:$COMMIT_SHA']
  
  # Deploy to Cloud Run
  - name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: gcloud
    args:
      - 'run'
      - 'deploy'
      - 'my-app'
      - '--image'
      - 'gcr.io/$PROJECT_ID/my-app:$COMMIT_SHA'
      - '--region'
      - 'us-central1'
      - '--platform'
      - 'managed'

images:
  - 'gcr.io/$PROJECT_ID/my-app:$COMMIT_SHA'
```

**Flujo del pipeline:**
```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  Push   │───►│  Build  │───►│  Test   │───►│ Deploy  │
│  Code   │    │  Image  │    │  (Unit) │    │ Cloud   │
│         │    │         │    │         │    │ Run     │
└─────────┘    └─────────┘    └─────────┘    └─────────┘
```

---

## Semana 4 — Data Engineering

### Curso
**Data Engineering on Google Cloud**  
⏱️ Duración sugerida: 3-4 horas

### Temas
- BigQuery
- Dataflow
- Dataproc
- Data Catalog

### Reto
📝 Crear flujo ETL simple (ingesta → procesamiento → resultado):

**Arquitectura ETL:**
```
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│   Ingesta     │    │ Procesamiento │    │   Resultado   │
│               │    │               │    │               │
│ Cloud Storage │───►│   Dataflow    │───►│   BigQuery    │
│ (Raw Data)    │    │   (Apache     │    │   (Data       │
│               │    │    Beam)      │    │    Warehouse) │
└───────────────┘    └───────────────┘    └───────────────┘
         │                   │                     │
         ▼                   ▼                     ▼
    CSV/JSON files    Transform/Clean      Analytics/BI
```

**Ejemplo de pipeline en Python (Apache Beam):**
```python
import apache_beam as beam

def run_pipeline():
    with beam.Pipeline() as pipeline:
        (
            pipeline
            | 'Read CSV' >> beam.io.ReadFromText('gs://bucket/raw/*.csv')
            | 'Parse' >> beam.Map(parse_csv)
            | 'Transform' >> beam.Map(transform_data)
            | 'Write to BQ' >> beam.io.WriteToBigQuery(
                'project:dataset.table',
                schema='...',
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
            )
        )
```

---

## Semana 5 — Machine Learning Básico en la Nube

### Curso
**ML for Production with Vertex AI**  
⏱️ Duración sugerida: 3-4 horas

### Temas
- Vertex AI Platform
- AutoML
- Custom Training
- Model Registry

### Reto
📝 Entrenar un modelo básico (clásico) con AutoML:

**Pasos:**
1. Preparar dataset (CSV con features y labels)
2. Crear Dataset en Vertex AI
3. Configurar entrenamiento AutoML
4. Evaluar métricas del modelo
5. Desplegar endpoint

**Métricas a evaluar:**
| Métrica | Descripción | Objetivo |
|---------|-------------|----------|
| Accuracy | % de predicciones correctas | > 85% |
| Precision | % de positivos verdaderos | > 80% |
| Recall | % de positivos detectados | > 80% |
| F1-Score | Balance precision/recall | > 0.8 |

**Ejemplo de predicción:**
```python
from google.cloud import aiplatform

endpoint = aiplatform.Endpoint(
    endpoint_name="projects/xxx/locations/us-central1/endpoints/xxx"
)

prediction = endpoint.predict(instances=[
    {"feature1": value1, "feature2": value2}
])
```

---

## Semana 6 — Seguridad Avanzada

### Curso
**Security and Identity Engineering on Google Cloud**  
⏱️ Duración sugerida: 3-4 horas

### Temas
- VPC Service Controls
- Binary Authorization
- Security Command Center
- Cloud Armor

### Reto
📝 Reglas de seguridad para app con 3 niveles de acceso:

**Niveles de acceso:**

| Nivel | Rol | Recursos | Acciones |
|-------|-----|----------|----------|
| Admin | Super usuario | Todos | CRUD + IAM |
| Editor | Desarrollador | Proyecto específico | CRUD |
| Viewer | Auditor | Logs y monitoreo | Solo lectura |

**Implementación con IAM:**
```yaml
# iam-bindings.yaml
bindings:
  - role: roles/owner
    members:
      - group:admins@company.com
    condition:
      title: "MFA Required"
      expression: "request.auth.claims.mfa == true"
  
  - role: roles/editor
    members:
      - group:developers@company.com
    condition:
      title: "Working Hours"
      expression: "request.time.getHours('America/Los_Angeles') >= 9 && request.time.getHours('America/Los_Angeles') <= 18"
  
  - role: roles/viewer
    members:
      - group:auditors@company.com
```

**Cloud Armor Policy:**
```yaml
# cloud-armor-policy.yaml
rules:
  - action: deny(403)
    priority: 1000
    match:
      expr:
        expression: "origin.region_code == 'CN'"
  
  - action: rate_limit
    priority: 2000
    rate_limit_options:
      rate_limit_threshold:
        count: 100
        interval_sec: 60
```

---

## Semana 7 — Cost Optimization

### Curso
**Cost Management Fundamentals**  
⏱️ Duración sugerida: 3-4 horas

### Temas
- Billing y Cost Management
- Committed Use Discounts (CUDs)
- Recomendaciones de optimización
- Budgets y alertas

### Reto
📝 Crear plan para bajar 20–30% de costos:

**Análisis actual:**
| Recurso | Costo Mensual | % del Total |
|---------|---------------|-------------|
| Compute Engine | $X | XX% |
| Cloud Storage | $X | XX% |
| BigQuery | $X | XX% |
| Network | $X | XX% |

**Estrategias de optimización:**

1. **Compute Engine (-25%):**
   - Usar VMs preemptibles para workloads batch
   - Rightsizing de instancias sobredimensionadas
   - Committed Use Discounts (1-3 años)

2. **Cloud Storage (-20%):**
   - Lifecycle policies para archivado automático
   - Migrar datos fríos a Nearline/Coldline
   - Eliminar objetos huérfanos

3. **BigQuery (-30%):**
   - Usar tablas particionadas
   - Configurar expiración de tablas
   - Optimizar queries (SELECT solo columnas necesarias)

4. **Networking (-15%):**
   - Optimizar tráfico entre regiones
   - Usar Cloud CDN para contenido estático
   - Comprimir datos en tránsito

**Plan de implementación:**
| Semana | Acción | Ahorro Esperado |
|--------|--------|-----------------|
| 1 | Rightsizing VMs | 10% |
| 2 | Storage lifecycle | 5% |
| 3 | BigQuery optimization | 8% |
| 4 | Review y ajustes | 7% |

---

## Semana 8 — Proyecto Final Avanzado

### Actividad
Crear una solución empresarial completa que incluya:

- ✅ Cloud Run + API
- ✅ Base de datos administrada
- ✅ Pipeline de datos
- ✅ Monitoreo completo
- ✅ CI/CD configurado

### Arquitectura propuesta

```
                              ┌─────────────────────────┐
                              │      Cloud CDN          │
                              └───────────┬─────────────┘
                                          │
                              ┌───────────▼─────────────┐
                              │   Global Load Balancer  │
                              └───────────┬─────────────┘
                                          │
                    ┌─────────────────────┼─────────────────────┐
                    │                     │                     │
          ┌─────────▼─────────┐ ┌─────────▼─────────┐ ┌─────────▼─────────┐
          │    Cloud Run      │ │    Cloud Run      │ │    Cloud Run      │
          │    (API v1)       │ │    (API v2)       │ │    (Workers)      │
          └─────────┬─────────┘ └─────────┬─────────┘ └─────────┬─────────┘
                    │                     │                     │
                    └─────────────────────┼─────────────────────┘
                                          │
                    ┌─────────────────────┼─────────────────────┐
                    │                     │                     │
          ┌─────────▼─────────┐ ┌─────────▼─────────┐ ┌─────────▼─────────┐
          │   Cloud SQL       │ │    Firestore      │ │   Cloud Storage   │
          │   (PostgreSQL)    │ │   (Cache/NoSQL)   │ │   (Objects)       │
          └───────────────────┘ └───────────────────┘ └───────────────────┘
                                          │
                              ┌───────────▼─────────────┐
                              │      Pub/Sub            │
                              │   (Event Streaming)     │
                              └───────────┬─────────────┘
                                          │
                              ┌───────────▼─────────────┐
                              │      Dataflow           │
                              │   (Data Processing)     │
                              └───────────┬─────────────┘
                                          │
                              ┌───────────▼─────────────┐
                              │      BigQuery           │
                              │   (Analytics)           │
                              └───────────┬─────────────┘
                                          │
          ┌───────────────────────────────┼───────────────────────────────┐
          │                               │                               │
┌─────────▼─────────┐         ┌───────────▼─────────────┐     ┌───────────▼─────────┐
│  Cloud Monitoring │         │     Cloud Logging       │     │   Error Reporting   │
└───────────────────┘         └─────────────────────────┘     └─────────────────────┘
```

### CI/CD Pipeline

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│  Push   │───►│  Build  │───►│  Test   │───►│ Staging │───►│  Prod   │
│  to Git │    │ & Scan  │    │ (Unit/  │    │ Deploy  │    │ Deploy  │
│         │    │         │    │ Integr) │    │         │    │         │
└─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘
                    │              │              │              │
                    ▼              ▼              ▼              ▼
               Container      Coverage       Canary        Full
               Security       Report         Release       Release
```

### Entregables

1. **Arquitectura completa:**
   - Diagrama detallado con todos los componentes
   - Justificación de cada decisión técnica
   - Estimación de costos mensuales

2. **Documentación técnica:**
   - README con instrucciones de despliegue
   - API documentation (OpenAPI/Swagger)
   - Runbook para operaciones

3. **Repositorio de código:**
   - Código fuente de la aplicación
   - Archivos de IaC (Terraform)
   - Configuración de CI/CD

4. **Checklist de seguridad:**

| Verificación | Estado |
|--------------|--------|
| Secretos en Secret Manager | ⬜ |
| SSL/TLS en todos los endpoints | ⬜ |
| WAF (Cloud Armor) configurado | ⬜ |
| VPC Service Controls | ⬜ |
| Audit logs habilitados | ⬜ |
| Backup y DR documentado | ⬜ |
| Compliance (SOC2/HIPAA si aplica) | ⬜ |

### Criterios de evaluación

| Criterio | Puntos |
|----------|--------|
| Arquitectura escalable y bien diseñada | 20 |
| Seguridad implementada correctamente | 20 |
| Pipeline de datos funcional | 15 |
| CI/CD completo | 15 |
| Monitoreo y observabilidad | 15 |
| Documentación profesional | 15 |

---

## 📊 Resumen del Progreso

| Semana | Tema | Estado |
|--------|------|--------|
| 1 | Arquitectura Escalable | ⬜ |
| 2 | Kubernetes Profesional | ⬜ |
| 3 | Serverless y Microservicios | ⬜ |
| 4 | Data Engineering | ⬜ |
| 5 | Machine Learning | ⬜ |
| 6 | Seguridad Avanzada | ⬜ |
| 7 | Cost Optimization | ⬜ |
| 8 | Proyecto Final | ⬜ |

---

## 🎓 Certificaciones Recomendadas

Después de completar esta ruta, considera obtener:

- [Google Cloud Professional Cloud Architect](https://cloud.google.com/certification/cloud-architect)
- [Google Cloud Professional Data Engineer](https://cloud.google.com/certification/data-engineer)
- [Google Cloud Professional DevOps Engineer](https://cloud.google.com/certification/cloud-devops-engineer)

---

## 🔗 Recursos Adicionales

- [Google Cloud Architecture Center](https://cloud.google.com/architecture)
- [Google Cloud Solutions](https://cloud.google.com/solutions)
- [SRE Books by Google](https://sre.google/books/)
- [GCP Pricing Calculator](https://cloud.google.com/products/calculator)

---

[← Ruta Intermedio](intermedio.md) | [Volver al inicio](../README.md)
