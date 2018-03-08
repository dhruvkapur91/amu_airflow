from airflow import DAG
from airflow.models import Variable
from airflow.operators.python_operator import BranchPythonOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

dag = DAG(
    dag_id = 'show_branch_operator', 
    description="This DAG shows branching, if there is no data for particular partition then it skips it, else does word count",
    start_date=datetime(2018,2,1),
    catchup=False,
    schedule_interval=timedelta(days=1))


def check_data_exists():
    import requests
    r = requests.get(Variable.get('data_base_url'))
    if r.status_code == 200:
        return 'process_data'
    else:
        return 'log_no_data'

does_data_exist = BranchPythonOperator(
    task_id = 'does_data_exist',
    python_callable = check_data_exists,
    dag = dag
)

process_data = BashOperator(
    task_id = 'process_data',
    dag = dag,
    bash_command = 'echo Processing data'
)

log_no_data = BashOperator(
    task_id = 'log_no_data',
    dag = dag,
    bash_command = 'echo No data found!'
)

process_data.set_upstream(does_data_exist)
log_no_data.set_upstream(does_data_exist)
