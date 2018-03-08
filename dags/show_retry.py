from airflow.models import DAG, Variable
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

dag = DAG(
    dag_id='show_retry',
    description="Sample to show how a retry might work",
    start_date=datetime(2018, 2, 20),
    catchup=False,
    schedule_interval=timedelta(days=1)
)

def fail_twice_before_succeeding():
    number_of_times_called = int(Variable.get('number_of_times_called'))
    if number_of_times_called < 2:
        number_of_times_called += 1
        Variable.set('number_of_times_called', str(number_of_times_called))
        raise Exception("Failing!")
    Variable.set('number_of_times_called',"0")
    print("Passed now!")

task_that_fails_2_times_before_succeeding = PythonOperator(
    task_id = 'some_task',
    python_callable = fail_twice_before_succeeding,
    retries = 3,
    retry_delay = timedelta(seconds=15),
    dag = dag
)
