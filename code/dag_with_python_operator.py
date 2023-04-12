from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'pratik',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

dag_info = {
    'id' : 'DAG_with_Python_Operator_V5',
    'description': 'This is our first dag with python operator',
    'start_date': datetime(2023, 4, 4, 2)
}

def greet(name, age):
    print(f'Name : {name}, Age : {age}')


dag = DAG (
    dag_id= dag_info['id'], 
    default_args=default_args, 
    description=dag_info['description'] , 
    start_date=dag_info['start_date'], 
    schedule_interval='@daily'
)
    
task1 = PythonOperator (
    task_id = 'greetings',
    python_callable = greet,
    op_kwargs={'name' : 'Pratik', 'age' : 22},
    dag = dag
)

#Build Dependencies
task1