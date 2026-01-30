# README: Configuración de CI/CD para Apache Airflow con GitHub Actions

## 📋 Guía Paso a Paso para Principiantes

Este tutorial te guiará para configurar un pipeline CI/CD completo para tus DAGs de Apache Airflow usando GitHub Actions.

---

## 🎯 ¿Qué vamos a lograr?

- ✅ Tests automáticos cada vez que hagas push
- ✅ Validación de sintaxis de DAGs
- ✅ Despliegue automático a diferentes ambientes
- ✅ Reporte de cobertura de código

---

## 📁 Estructura del Proyecto

Primero, crea esta estructura en tu repositorio:

```
mi-proyecto-airflow/
├── .github/
│   └── workflows/
│       └── ci-cd-airflow.yml
├── dags/
│   └── etl_pipeline.py
├── tests/
│   └── dags/
│       ├── test_etl_pipeline.py
│       └── test_dag_integration.py
├── scripts/
│   └── deploy.sh
├── requirements.txt
└── README.md
```

---

## 🚀 PASO 1: Preparar tu Repositorio

### 1.1 Crear el repositorio en GitHub

1. Ve a GitHub.com
2. Click en "New repository"
3. Nombre: `airflow-cicd-tutorial`
4. Marca "Add a README file"
5. Click "Create repository"

### 1.2 Clonar el repositorio localmente

```bash
git clone https://github.com/TU-USUARIO/airflow-cicd-tutorial.git
cd airflow-cicd-tutorial
```

---

## 📝 PASO 2: Crear el DAG de Ejemplo

### 2.1 Crear la carpeta de DAGs

```bash
mkdir -p dags
```

### 2.2 Crear tu primer DAG

Crea el archivo `dags/etl_pipeline.py`:

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Configuración por defecto
default_args = {
    'owner': 'tu-nombre',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

# Definir el DAG
dag = DAG(
    'etl_pipeline',
    default_args=default_args,
    description='Pipeline ETL de ejemplo para CI/CD',
    schedule_interval='@daily',
    catchup=False,
    tags=['example', 'etl'],
)

# Funciones de las tareas
def extract_data():
    print("📥 Extrayendo datos...")
    return {"status": "success", "records": 100}

def transform_data():
    print("🔄 Transformando datos...")
    return {"status": "transformed", "records": 95}

def load_data():
    print("📤 Cargando datos...")
    return {"status": "loaded"}

# Definir tareas
start = BashOperator(
    task_id='start',
    bash_command='echo "Iniciando pipeline ETL"',
    dag=dag,
)

extract = PythonOperator(
    task_id='extract',
    python_callable=extract_data,
    dag=dag,
)

transform = PythonOperator(
    task_id='transform',
    python_callable=transform_data,
    dag=dag,
)

load = PythonOperator(
    task_id='load',
    python_callable=load_data,
    dag=dag,
)

end = BashOperator(
    task_id='end',
    bash_command='echo "✅ Pipeline completado"',
    dag=dag,
)

# Definir dependencias
start >> extract >> transform >> load >> end
```

---

## 🧪 PASO 3: Crear los Tests

### 3.1 Crear estructura de tests

```bash
mkdir -p tests/dags
```

### 3.2 Crear archivo de tests

Crea `tests/dags/test_etl_pipeline.py`:

```python
import pytest
from airflow.models import DagBag
from datetime import datetime, timedelta

class TestETLPipeline:
    
    @pytest.fixture(scope='class')
    def dagbag(self):
        """Cargar DAGs una vez por clase de tests"""
        return DagBag(dag_folder='dags/', include_examples=False)
    
    def test_dag_loaded(self, dagbag):
        """Verificar que el DAG se carga correctamente"""
        dag = dagbag.get_dag('etl_pipeline')
        assert dag is not None, "❌ DAG etl_pipeline no encontrado"
        print("✅ DAG cargado correctamente")
    
    def test_dag_has_tasks(self, dagbag):
        """Verificar que el DAG tiene tareas"""
        dag = dagbag.get_dag('etl_pipeline')
        assert len(dag.tasks) >= 5, f"❌ DAG tiene solo {len(dag.tasks)} tareas"
        print(f"✅ DAG tiene {len(dag.tasks)} tareas")
    
    def test_task_dependencies(self, dagbag):
        """Verificar dependencias entre tareas"""
        dag = dagbag.get_dag('etl_pipeline')
        
        extract = dag.get_task('extract')
        transform = dag.get_task('transform')
        load = dag.get_task('load')
        
        assert transform in extract.downstream_list, "❌ Transform no depende de extract"
        assert load in transform.downstream_list, "❌ Load no depende de transform"
        print("✅ Dependencias correctas")
    
    def test_dag_schedule(self, dagbag):
        """Verificar configuración de scheduling"""
        dag = dagbag.get_dag('etl_pipeline')
        assert dag.schedule_interval is not None, "❌ DAG sin schedule"
        print(f"✅ Schedule: {dag.schedule_interval}")
```

Crea `tests/dags/test_dag_integration.py`:

```python
import pytest
from airflow.models import DagBag

class TestDAGIntegration:
    
    @pytest.fixture(scope='class')
    def dagbag(self):
        return DagBag(dag_folder='dags/', include_examples=False)
    
    def test_no_import_errors(self, dagbag):
        """Verificar que no hay errores de importación"""
        assert not dagbag.import_errors, f"❌ Errores: {dagbag.import_errors}"
        print("✅ Sin errores de importación")
    
    def test_dag_no_cycles(self, dagbag):
        """Verificar que no hay ciclos en dependencias"""
        dag = dagbag.get_dag('etl_pipeline')
        # El método test_cycle() devuelve False si NO hay ciclos
        assert dag.test_cycle() == False, "❌ DAG tiene ciclos"
        print("✅ Sin ciclos de dependencias")
```

### 3.3 Crear archivo de requirements

Crea `requirements.txt`:

```
apache-airflow==2.7.0
pytest==7.4.3
pytest-cov==4.1.0
```

---

## ⚙️ PASO 4: Configurar GitHub Actions

### 4.1 Crear carpeta de workflows

```bash
mkdir -p .github/workflows
```

### 4.2 Crear el workflow de CI/CD

Crea `.github/workflows/ci-cd-airflow.yml`:

```yaml
name: Airflow CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  AIRFLOW_VERSION: 2.7.0
  PYTHON_VERSION: '3.9'

jobs:
  test:
    name: 🧪 Test DAGs
    runs-on: ubuntu-latest
    
    steps:
    - name: 📥 Checkout código
      uses: actions/checkout@v3
    
    - name: 🐍 Configurar Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ env.PYTHON_VERSION }}
    
    - name: 📦 Instalar dependencias
      run: |
        pip install --upgrade pip
        pip install apache-airflow==${{ env.AIRFLOW_VERSION }}
        pip install pytest pytest-cov
    
    - name: ✅ Validar sintaxis de DAGs
      run: |
        python -c "
        from airflow.models import DagBag
        dagbag = DagBag(dag_folder='dags/', include_examples=False)
        if dagbag.import_errors:
            print('❌ ERRORES EN DAGs:', dagbag.import_errors)
            exit(1)
        print(f'✅ {len(dagbag.dags)} DAGs cargados correctamente')
        "
    
    - name: 🧪 Ejecutar tests
      run: |
        pytest tests/dags/ -v --cov=dags --cov-report=xml --cov-report=term
    
    - name: 📊 Subir reporte de cobertura
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella
        fail_ci_if_error: false

  deploy-dev:
    name: 🚀 Deploy a Dev
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/develop'
    
    steps:
    - name: 📥 Checkout código
      uses: actions/checkout@v3
    
    - name: 🚀 Deploy a Development
      run: |
        echo "🔧 Desplegando a ambiente de desarrollo..."
        echo "✅ Deployment exitoso"

  deploy-prod:
    name: 🎯 Deploy a Producción
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: production
    
    steps:
    - name: 📥 Checkout código
      uses: actions/checkout@v3
    
    - name: 🎯 Deploy a Production
      run: |
        echo "🚀 Desplegando a producción..."
        echo "✅ Deployment a producción exitoso"
```

---

## 🔄 PASO 5: Subir Código a GitHub

```bash
# Agregar todos los archivos
git add .

# Crear commit
git commit -m "Configuración inicial de CI/CD para Airflow"

# Subir a GitHub
git push origin main
```

---

## 👀 PASO 6: Verificar que Funciona

### 6.1 Ver el workflow en acción

1. Ve a tu repositorio en GitHub
2. Click en la pestaña "Actions"
3. Deberías ver tu workflow ejecutándose
4. Click en el workflow para ver los detalles

### 6.2 Verificar que los tests pasan

En la sección "Jobs" deberías ver:
- ✅ Test DAGs (verde si todo está bien)
- ✅ Deploy a Producción (si hiciste push a main)

---

## 🧪 PASO 7: Probar Localmente (Opcional)

### 7.1 Instalar dependencias

```bash
pip install -r requirements.txt
```

### 7.2 Ejecutar tests

```bash
# Ejecutar todos los tests
pytest tests/dags/ -v

# Ejecutar con cobertura
pytest tests/dags/ -v --cov=dags --cov-report=term
```

### 7.3 Validar DAGs manualmente

```bash
python -c "
from airflow.models import DagBag
dagbag = DagBag(dag_folder='dags/', include_examples=False)
print(f'DAGs encontrados: {len(dagbag.dags)}')
for dag_id in dagbag.dag_ids:
    print(f'  - {dag_id}')
"
```

---

## 🌿 PASO 8: Trabajar con Branches

### 8.1 Crear rama de desarrollo

```bash
# Crear y cambiar a rama develop
git checkout -b develop

# Hacer cambios en tu DAG
# ... editar archivos ...

# Commit y push
git add .
git commit -m "Nuevas features en DAG"
git push origin develop
```

Esto activará el workflow y desplegará a "dev" automáticamente.

### 8.2 Crear Pull Request

1. Ve a GitHub
2. Click en "Pull requests"
3. Click "New pull request"
4. Selecciona `develop` → `main`
5. Los tests se ejecutarán automáticamente
6. Si pasan, puedes hacer merge

---

## 🎓 Conceptos Clave

### ¿Qué es CI/CD?

- **CI (Continuous Integration)**: Tests automáticos al hacer cambios
- **CD (Continuous Deployment)**: Despliegue automático cuando los tests pasan

### ¿Por qué es importante para DAGs?

1. **Prevenir errores**: Detecta problemas antes de producción
2. **Confianza**: Sabes que tu código funciona
3. **Rapidez**: Deploy automático sin pasos manuales
4. **Trazabilidad**: Historial de todos los cambios

---

## 🔧 Troubleshooting

### Error: "DAG not found"

```bash
# Verifica que la estructura sea correcta
ls -la dags/
# Debe mostrar etl_pipeline.py
```

### Error: "Module not found"

```bash
# Reinstala dependencias
pip install -r requirements.txt
```

### El workflow no se ejecuta

- Verifica que el archivo esté en `.github/workflows/`
- Verifica que hiciste push a `main` o `develop`
- Revisa la pestaña "Actions" en GitHub

---

## 📚 Próximos Pasos

1. ✅ Agrega más DAGs a la carpeta `dags/`
2. ✅ Crea más tests en `tests/dags/`
3. ✅ Configura ambientes reales (Docker, Kubernetes)
4. ✅ Agrega notificaciones (Slack, Email)
5. ✅ Implementa métricas y monitoring

---

## 🤝 ¿Necesitas Ayuda?

- Revisa los logs en la pestaña "Actions" de GitHub
- Cada step muestra output detallado
- Los errores aparecen en rojo con descripciones

---

## ✅ Checklist Final

- [ ] Repositorio creado en GitHub
- [ ] Estructura de carpetas correcta
- [ ] DAG creado en `dags/`
- [ ] Tests creados en `tests/dags/`
- [ ] Workflow en `.github/workflows/`
- [ ] Código subido a GitHub
- [ ] Workflow ejecutándose correctamente
- [ ] Tests pasando (verde en Actions)

