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