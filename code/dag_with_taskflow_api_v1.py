from datetime import datetime, timedelta
from airflow.decorators import dag, task


default_args = {
    'owner': 'pratik',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

@task(multiple_outputs=True)
def get_name():
    return { 'first_name': 'Pratik' ,'last_name': 'Kakadiya'}

@task()
def get_age():
    return 22

@task()
def greet(first_name, last_name, age):
    print(f" First Name : {first_name}, Last Name : {last_name}, Age: {age}")


@dag(
        dag_id='dag_with_taskflow_api_v05', 
        default_args=default_args, 
        start_date=datetime(2023, 4, 4, 2), 
        schedule_interval='@daily'
    )
def hello_world_etl():    
    name_dict = get_name()
    age = get_age()
    greet(first_name=name_dict['first_name'], last_name=name_dict['last_name'], age=age)

#greet_dag = 
hello_world_etl()