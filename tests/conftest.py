import os
import pytest

# Configurar variables de entorno para tests
os.environ['AIRFLOW__CORE__UNIT_TEST_MODE'] = 'True'
os.environ['AIRFLOW__CORE__LOAD_EXAMPLES'] = 'False'
os.environ['AIRFLOW__CORE__DAGS_FOLDER'] = 'dags/'

# Desactivar la carga de configuración de Airflow
os.environ['AIRFLOW__CORE__LOAD_DEFAULT_CONNECTIONS'] = 'False'

@pytest.fixture(scope='session', autouse=True)
def setup_test_environment():
    """Configurar ambiente de testing antes de ejecutar tests"""
    print("\n🔧 Configurando ambiente de testing...")
    yield
    print("\n✅ Tests completados")