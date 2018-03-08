from airflow import DAG 
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

dag = DAG(dag_id = 'show_start_date', description="This is my first dag!", start_date=datetime(2018,2,1), schedule_interval=timedelta(days=1))

print_todays_date = BashOperator(
    task_id = "print_todays_date",
    bash_command = "date",
    dag = dag
)