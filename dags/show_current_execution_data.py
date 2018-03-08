"""
Should start from 1st Feb and run every day and print the date!
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

dag = DAG(dag_id='show_current_execution_date', description="Should start from 1st Feb and run every day and print the date!",
          start_date=datetime(2018, 2, 1), schedule_interval=timedelta(days=1))

print_execution_date = BashOperator(
    task_id="print_execution_date",
    bash_command="echo {{ ds}} ",
    dag=dag
)

print_execution_date.doc_md = "Print tasks execution date"
