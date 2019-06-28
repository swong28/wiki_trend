# import airflow packages
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator

# other packages
from datetime import datetime
from datetime import timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2019, 06, 20),
    'email_on_failure': False,
    'email_on_retry': False,
    'schedule_interval': '@monthly',
    'retries': 1,
    'retry_delay': timedelta(days=1),
}