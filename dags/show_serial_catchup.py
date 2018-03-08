from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

default_args = {
    'depends_on_past' : True
}

dag = DAG(
    dag_id='show_serial_catchup', 
    description="This DAG is supposed to execute things one by one (left to right), and not concurrent!",
    start_date=datetime(2018, 2, 1), 
    schedule_interval=timedelta(days=1),
    default_args=default_args
)

print_todays_date = BashOperator(
    task_id="print_todays_date",
    bash_command="date",
    dag=dag
)
