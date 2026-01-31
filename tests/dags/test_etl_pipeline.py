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
        
        # Verificar que extract tiene transform como downstream
        assert transform in extract.downstream_list, \
            f"❌ Transform no está en downstream de extract. Downstream actual: {[t.task_id for t in extract.downstream_list]}"
        
        # Verificar que transform tiene load como downstream
        assert load in transform.downstream_list, \
            f"❌ Load no está en downstream de transform. Downstream actual: {[t.task_id for t in transform.downstream_list]}"
        
        print("✅ Dependencias correctas:")
        print(f"   extract -> {[t.task_id for t in extract.downstream_list]}")
        print(f"   transform -> {[t.task_id for t in transform.downstream_list]}")
        print(f"   load -> {[t.task_id for t in load.downstream_list]}")
    
    def test_dag_schedule(self, dagbag):
        """Verificar configuración de scheduling"""
        dag = dagbag.dags['etl_pipeline']
        # En Airflow 2.7, schedule_interval puede ser None si se usa 'schedule'
        assert dag.schedule_interval is not None or dag.timetable is not None, \
            "❌ DAG sin schedule definido"
        print(f"✅ Schedule configurado")
    
    def test_all_tasks_have_owners(self, dagbag):
        """Verificar que todas las tareas tienen owner"""
        dag = dagbag.dags['etl_pipeline']
        for task in dag.tasks:
            assert task.owner is not None, f"❌ Tarea {task.task_id} sin owner"
        print("✅ Todas las tareas tienen owner")
    
    def test_critical_tasks_exist(self, dagbag):
        """Verificar que las tareas críticas existen"""
        dag = dagbag.dags['etl_pipeline']
        
        required_tasks = ['start', 'extract', 'transform', 'load', 'end']
        task_ids = [t.task_id for t in dag.tasks]
        
        for required_task in required_tasks:
            assert required_task in task_ids, \
                f"❌ Tarea requerida '{required_task}' no encontrada"
        
        print(f"✅ Todas las tareas críticas existen: {required_tasks}")
