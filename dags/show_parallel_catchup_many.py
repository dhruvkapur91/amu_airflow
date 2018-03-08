from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

default_args = {
    'depends_on_past': False
}

dag = DAG(
    dag_id='show_parallel_catchup_many',
    description="This DAG is supposed to execute stuff in parallel, no order really!",
    start_date=datetime(2018, 2, 1),
    schedule_interval=timedelta(days=1),
    default_args=default_args
)

sleep_for_five_seconds = BashOperator(
    task_id="sleep_for_five_seconds",
    bash_command="sleep 5",
    dag=dag
)

sleep_for_two_seconds = BashOperator(
    task_id="sleep_for_two_seconds",
    bash_command="sleep 2",
    dag=dag
)
