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
        dag = dagbag.dags['etl_pipeline']
        # Verificar manualmente que no hay ciclos
        # El método test_cycle() devuelve False si NO hay ciclos
        has_cycle = dag.test_cycle()
        assert has_cycle == False, "❌ DAG tiene ciclos"
        print("✅ Sin ciclos de dependencias")
    
    def test_dag_tags(self, dagbag):
        """Verificar que el DAG tiene tags"""
        dag = dagbag.dags['etl_pipeline']
        assert dag.tags is not None, "❌ DAG sin tags"
        assert len(dag.tags) > 0, "❌ DAG sin tags definidos"
        print(f"✅ Tags encontrados: {dag.tags}")
    
    def test_task_retries(self, dagbag):
        """Verificar que las tareas tienen retries configurados"""
        dag = dagbag.dags['etl_pipeline']
        for task in dag.tasks:
            assert task.retries >= 1, f"❌ Tarea {task.task_id} sin retries"
        print("✅ Todas las tareas tienen retries configurados")