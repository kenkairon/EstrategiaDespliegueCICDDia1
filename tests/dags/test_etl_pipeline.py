import pytest
from airflow.models import DagBag
from datetime import datetime

class TestETLPipeline:
    
    @pytest.fixture(scope='class')
    def dagbag(self):
        """Cargar DAGs una vez por clase de tests"""
        return DagBag(dag_folder='dags/', include_examples=False)
    
    def test_dag_loaded(self, dagbag):
        """Verificar que el DAG se carga correctamente"""
        # Acceder directamente al diccionario de DAGs sin usar get_dag()
        assert 'etl_pipeline' in dagbag.dags, "❌ DAG etl_pipeline no encontrado"
        dag = dagbag.dags['etl_pipeline']
        assert dag.description is not None, "❌ DAG sin descripción"
        print("✅ DAG cargado correctamente")
    
    def test_dag_has_tasks(self, dagbag):
        """Verificar que el DAG tiene tareas"""
        dag = dagbag.dags['etl_pipeline']
        assert len(dag.tasks) >= 5, f"❌ DAG tiene solo {len(dag.tasks)} tareas"
        print(f"✅ DAG tiene {len(dag.tasks)} tareas")
    
    def test_task_dependencies(self, dagbag):
        """Verificar dependencias entre tareas"""
        dag = dagbag.dags['etl_pipeline']
        
        extract = dag.get_task('extract')
        transform = dag.get_task('transform')
        load = dag.get_task('load')
        
        assert transform in extract.downstream_list, "❌ Transform no depende de extract"
        assert load in transform.downstream_list, "❌ Load no depende de transform"
        print("✅ Dependencias correctas")
    
    def test_dag_schedule(self, dagbag):
        """Verificar configuración de scheduling"""
        dag = dagbag.dags['etl_pipeline']
        assert dag.schedule_interval is not None, "❌ DAG sin schedule"
        print(f"✅ Schedule: {dag.schedule_interval}")
    
    def test_all_tasks_have_owners(self, dagbag):
        """Verificar que todas las tareas tienen owner"""
        dag = dagbag.dags['etl_pipeline']
        for task in dag.tasks:
            assert task.owner is not None, f"❌ Tarea {task.task_id} sin owner"
        print("✅ Todas las tareas tienen owner")