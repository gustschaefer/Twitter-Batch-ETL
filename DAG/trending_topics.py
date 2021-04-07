from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from ETL_scripts.load_to_s3 import local_to_s3

# Teste simples para verificar se o carregamento esta sendo feito corretamente

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

    start = DummyOperator(task_id='start_of_data_pipeline', dag=dag)

    trending_to_s3 = PythonOperator(
    task_id='parquet_files_to_s3',
    python_callable=local_to_s3,
    )

    end = DummyOperator(task_id='end_of_data_pipeline', dag=dag)

start >> trending_to_s3 >> end
