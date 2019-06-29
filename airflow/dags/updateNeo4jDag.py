# import airflow packages
from airflow import DAG
from airflow.contrib.operators import SSHOperator

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

now = datetime.now()

dag = DAG('ssh_operator', 
          default_args=default_args, 
          schedule_interval=timedelta(days=1))

t1 = SSHOperator(task_id='new_file_to_spark', 
                 ssh_conn_id="remote_vm_conn", 
                 command="python3 ./wiki-trend/s3Storing.py s3a://insight-wiki-clickstream/clickstream-enwiki-"+str(now.year)+"-"+str(now.month)+".tsv", 
                 dag=dag)

t2 = SSHOperator(task_id='load_to_neo4j',
                 ssh_conn_id="neo4j_conn",
                 command="source ./wiki-trend/spark/code/run.sh",
                 dag=dag)

t2.set_upstream(t1)






