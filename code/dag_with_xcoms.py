from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator


default_args = {
    'owner': 'pratik',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

dag_info = {
    'id' : 'dag_with_xcoms_v1',
    'description': 'This is our first dag with xcoms',
    'start_date': datetime(2023, 4, 4, 2)
}


def push_values(ti):
    ti.xcom_push(key='first_name', value='Pratik')
    ti.xcom_push(key='last_name', value='Kakadiya')

def pull_values(ti):
    first_name = ti.xcom_pull(task_ids='push_values', key='first_name')
    last_name = ti.xcom_pull(task_ids='push_values', key='last_name')
    print(f" First Name : {first_name}, Last Name : {last_name}")



dag = DAG (
    dag_id= dag_info['id'], 
    default_args=default_args, 
    description=dag_info['description'] , 
    start_date=dag_info['start_date'], 
    schedule_interval='@daily'
)
    
task1 = PythonOperator (
    task_id = 'push_values',
    python_callable = push_values,
    dag = dag
)

task2 = PythonOperator (
    task_id = 'pull_values',
    python_callable = pull_values,
    dag = dag
)

#Build Dependencies
task1 >> task2