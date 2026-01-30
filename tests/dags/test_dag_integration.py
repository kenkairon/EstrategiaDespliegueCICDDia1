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