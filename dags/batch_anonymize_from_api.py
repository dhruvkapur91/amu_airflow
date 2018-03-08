"""
This DAG make a GET request every day to get companies whose data for the day must be anonymized.
The GET request is on HTTP connection `pending_anonymization`, with url `pending_anonymization/day`
And clears the respective data from `data_postgres`, table `potential_clients`
"""

from airflow import DAG
from airflow.operators.http_operator import SimpleHttpOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.postgres_operator import PostgresOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from airflow.hooks.base_hook import BaseHook
import ast


args = {
    'depends_on_past': True,
}

dag = DAG(
    dag_id='batch_anonymize_from_api_v1',
    start_date=datetime(2018, 2, 10),
    schedule_interval=timedelta(days=1),
    default_args=args
)

dag.doc_md = __doc__


def debug_xcom_func(**kwargs):
    ti = kwargs['ti']
    print(type(ti.xcom_pull(task_ids='get_companies_pending_anonymization')))


def parse_companies_pending_anonymization_f(**kwargs):
    task_instance = kwargs['ti']
    get_companies_pending_anonymization_xcom = task_instance.xcom_pull(
        task_ids='get_companies_pending_anonymization')
    companies = ast.literal_eval(get_companies_pending_anonymization_xcom)[
        'companies_pending_anonymization'][1:-1].split(",")
    return ",".join([f"'{company}'" for company in companies])


with dag:
    get_companies_pending_anonymization = SimpleHttpOperator(
        task_id="get_companies_pending_anonymization",
        method='GET',
        http_conn_id='pending_anonymization',
        endpoint='pending_anonymization/{{ ds_nodash }}',
        xcom_push=True
    )

    parse_companies_pending_anonymization = PythonOperator(
        task_id="parse_companies_pending_anonymization",
        python_callable=parse_companies_pending_anonymization_f,
        provide_context=True
    )

    anonymize_companies_pending_for_anonymization = PostgresOperator(
        task_id="anonymize_companies_pending_for_anonymization",
        postgres_conn_id='data_postgres',
        autocommit=True,
        sql="update potential_clients set email = '' where company in ({{ task_instance.xcom_pull(task_ids='parse_companies_pending_anonymization') }}) and day = '{{ ds_nodash}}' ",
        retries=100,
        retry_delay=timedelta(seconds=45)
    )

    get_companies_pending_anonymization >> parse_companies_pending_anonymization >> anonymize_companies_pending_for_anonymization
