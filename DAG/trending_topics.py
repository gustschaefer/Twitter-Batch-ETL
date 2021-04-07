from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from ETL_scripts.load_to_s3 import local_to_s3
from ETL_scripts.config import bucket_name, temp_parquet_files


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2021, 4, 6),
    "retries": 0,
}

with DAG(
    "Twitter_Batch_ETL", 
    schedule_interval=timedelta(minutes=1),
    catchup=False,
    default_args=default_args
) as dag:

    # Inicio do Pipeline
    start_of_data_pipeline = DummyOperator(task_id='start_of_data_pipeline', dag=dag)

    trending_to_s3 = PythonOperator(
    task_id='parquet_files_to_s3',
    python_callable=local_to_s3,
    op_kwargs={
            'bucket_name': bucket_name, 
            'parquet_filepath': temp_parquet_files
    },
)

    # Fim da Pipeline
    end_of_data_pipeline = DummyOperator(task_id='end_of_data_pipeline', dag=dag)

# Definição do padrão de execução
start_of_data_pipeline >> trending_to_s3 >> end_of_data_pipeline