"""
This DAG make a GET request every day to get companies whose data for the day must be anonymized.
The GET request is on HTTP connection `pending_anonymization`, with url `pending_anonymization/day`
And prints the companies in the log for which anonymization needs to happen.
"""

from airflow import DAG
from airflow.operators.http_operator import SimpleHttpOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.postgres_operator import PostgresOperator
from datetime import datetime, timedelta
from airflow.hooks.base_hook import BaseHook


args = {
    'depends_on_past' : True,
}

dag = DAG(
    dag_id='batch_get_from_api_v1',
    start_date=datetime(2018, 2, 10),
    schedule_interval=timedelta(days=1),
    default_args=args
)

dag.doc_md = __doc__

with dag:
    get_companies_pending_anonymization = SimpleHttpOperator(
        task_id="get_companies_pending_anonymization",
        method='GET',
        http_conn_id='pending_anonymization',
        endpoint='pending_anonymization/{{ ds_nodash }}',
        xcom_push=True
    )

    print_companies_pending_anonymization = BashOperator(
        task_id="print_companies_pending_anonymization",
        bash_command="echo the anonymization API for {{ ds }} returned {{ task_instance.xcom_pull(task_ids='get_companies_pending_anonymization') }}"
    )

    get_companies_pending_anonymization >> print_companies_pending_anonymization
