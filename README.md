# Airflow

Apache Airflow is an open-source platform used for programmatically authoring, scheduling, and monitoring workflows. Airflow allows you to create and manage complex workflows as directed acyclic graphs (DAGs) of tasks, where each task represents a unit of work to be executed.

Airflow provides a web-based user interface where you can visualize and monitor the status of your workflows, as well as define the dependencies between tasks. It also offers a wide range of integrations with other tools and services, such as databases, cloud platforms, messaging queues, and more, making it a versatile and extensible tool for data engineering and other data-related tasks.

One of the key benefits of using Airflow is its ability to handle complex workflows with multiple dependencies and conditional logic, allowing you to create scalable and reliable data pipelines. Additionally, Airflow is highly customizable, so you can tailor it to your specific needs and use cases.

It is Written in Python

### **DAFs, Tasks & Operator**

**DAG** is the collection of all the tasks we want to run organized in a way that reflects the relationships and dependencies

**Task** defines the unit of work within DAG (Here A B C D E are the tasks) it is represented as a node in the DAG graph and it is written in Python. There are dependencies between Tasks Ex. Task C is downstream of Task A. Task C is also upstream of Task E.

The goal of the task is to achieve a specific thing, the method it uses is called the **Operator.** While DAGs describe how to run a workflow **Operators determine what actually gets done by a Task**

There are various kinds of Operators

- BashOperator
- PythonOperator
- Customised Operators can also be written

Each task in an implementation of an operator Ex. PythonOperator to execute the Python code or BashOperator to execute the bash command

![Untitled](https://github.com/pratik-18/Airflow/blob/main/images/img_1.png)

**Overview:** The operator determines what is going to be done. The Task implements an Operator by defining specific values for that Operator & The DAG collection of all the Tasks we want to run, organized in the way it reflects their relationship and dependencies 

![Untitled](https://github.com/pratik-18/Airflow/blob/main/images/img_2.png)

### Task Lifecycle

**There are in total 11 different kinds of stages in the Airflow UI**

![Untitled](https://github.com/pratik-18/Airflow/blob/main/images/img_3.png)

**Hierarchy in which status gets changed**

![Untitled](https://github.com/pratik-18/Airflow/blob/main/images/img_4.png)

### **Create a DAG**

The structure of the DAG looks as follows

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'pratik',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

dag_info = {
    'id': 'DAG_with_Python_Operator_V5',
    'description': 'This is our first dag with python operator',
    'start_date': datetime(2023, 4, 4, 2)
}

def greet(name, age):
    print(f'Name : {name}, Age : {age}')

# Create a DAG as follows and pass the necessary parameters
dag = DAG (
    dag_id= dag_info['id'], 
    default_args=default_args, 
    description=dag_info['description'] , 
    start_date=dag_info['start_date'], 
    schedule_interval='@daily'
)
   
# Now we have to define the tasks & do not forget to provide DAG
task1 = PythonOperator (
    task_id = 'greetings',
    python_callable = greet,
    op_kwargs={'name' : 'Pratik', 'age' : 22},
    dag = dag
)

#Build Dependencies (Define the sequence in which tasks will run) 
task1
```

> Note: In the above example we have passed parameters as well to the Python function using `op_kwargs`. We just have to pass the dictionary with the parameters that will be unpacked whenever the function is invoked.
> 

**Way to build dependencies**

If we assume that we have three tasks and we want to run **task1** first and after that **task2 & task3** at the same time then the following are the ways to accomplish that.

```python
# Task dependency method 1
    task1.set_downstream(task2)
    task1.set_downstream(task3)

# Task dependency method 2
    task1 >> task2
    task1 >> task3

# Task dependency method 3
    task1 >> [task2, task3]
```

### Sharing information between different Tasks

To achieve this we need to use Airflow XComs

Basically, we can push the information to XComs in one task and pull information in other tasks. By default, every function’s return value will be automatically pushed into XComs

```python
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
		#Push the value
    ti.xcom_push(key='first_name', value='Pratik')
    ti.xcom_push(key='last_name', value='Kakadiya')

def pull_values(ti):
		#Pull the value
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
```

Although it is very convenient to use for sharing values between tasks but we should be aware of the fact that the maximum size of XComs is only **48KB**

### **Airflow Taskflow API**

The Taskflow API in Airflow is a higher-level API built on top of Airflow's core DAG and task management infrastructure. It allows you to define complex workflows using a more intuitive and flexible programming interface, making it easier to express dependencies between tasks and handle errors and retries.

With Taskflow, you can define a DAG as a collection of tasks, where each task is an instance of a Task class that encapsulates the logic and dependencies of that task. These tasks can then be linked together using TaskFlow APIs to form a workflow.

Here is an example of that

```python
from datetime import datetime, timedelta
from airflow.decorators import dag, task

default_args = {
    'owner': 'pratik',
    'retries': 5,
    'retry_delay': timedelta(minutes=2)
}

#Create all the task & annotate it with @task decorator

#In the following task as we are sending a dictionary 
#we have to pass, multipe_outputs=True
@task(multiple_outputs=True)
def get_name():
    return { 'first_name': 'Pratik' ,'last_name': 'Kakadiya'}

@task()
def get_age():
    return 22

@task()
def greet(first_name, last_name, age):
    print(f" First Name : {first_name}, Last Name : {last_name}, Age: {age}")

#Procedure here as well is the same create a function and annotate it with the DAG decorator
@dag(
        dag_id='dag_with_taskflow_api_v05', 
        default_args=default_args, 
        start_date=datetime(2023, 4, 4, 2), 
        schedule_interval='@daily'
    )

#Call all the Tasks here as a normal function
def hello_world_etl():    
    name_dict = get_name()
    age = get_age()
    greet(first_name=name_dict['first_name'], last_name=name_dict['last_name'], age=age)

hello_world_etl()
```

Here is one more example but here we have used **BashOperator + PythonOperator** and also we have grouped tasks together using `TaskGroup()` function

```python
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.task_group import TaskGroup
from airflow.decorators import dag, task

# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'retries': 1
}

# Define the DAG using TaskFlow
@dag(default_args=default_args, schedule_interval=None, catchup=False)
def example_taskflow_dag():

    # Define a task group to group our tasks together
    task_group = TaskGroup('example_task_group', dag=example_taskflow_dag)

    # Define a BashOperator task to print a message
    task1 = BashOperator(
        task_id='task1',
        bash_command='echo "Hello from BashOperator!"',
        dag=example_taskflow_dag,
        task_group=task_group
    )

    # Define a PythonOperator task to print a message
    @task
    def task2():
        print('Hello from PythonOperator!')

    task2 = PythonOperator(
        task_id='task2',
        python_callable=task2,
        dag=example_taskflow_dag,
        task_group=task_group
    )

    # Define the dependencies between the tasks
    task1 >> task2

example_taskflow_dag = example_taskflow_dag()
```

**Which one is the better method for creating DAG with or without Taskflow API?**

The choice between using the traditional Airflow DAG definition syntax and the newer TaskFlow API ultimately comes down to personal preference and the specific requirements of your DAG.

Here are some factors to consider when deciding which approach to use:

**The complexity of the DAG**: If your DAG is relatively simple with only a few tasks and simple dependencies, you may find that the traditional Airflow DAG definition syntax is sufficient. However, if your DAG is more complex with many tasks and dependencies, the TaskFlow API can make it easier to manage and organize your tasks.

**Desired level of abstraction**: The TaskFlow API provides a higher level of abstraction than the traditional DAG definition syntax, which can make it easier to define and manage complex DAGs. However, if you prefer to have more control over the details of your DAG, you may find the traditional syntax to be more flexible.

**Developer experience and preferences:** Some developers may prefer the TaskFlow API because it is more Pythonic and provides a more streamlined way to define tasks and dependencies. Others may prefer the traditional syntax because it is more familiar and provides a more granular level of control over the DAG.

In summary, both approaches have their strengths and weaknesses, and the choice between them will depend on your specific requirements and preferences. It's worth experimenting with both approaches to see which one works best for you and your team.

### Catchup & Backfill

**Catchup** 

“Catchup" in Apache Airflow refers to the process of triggering and running all the previously scheduled DAG (Directed Acyclic Graph) runs that were missed during a period of inactivity or downtime.

When you enable catchup in Airflow, the scheduler will automatically schedule and execute all the tasks that were missed during the inactive period. This feature can be useful in situations where Airflow is down or when new DAGs are added to the system, as it ensures that no tasks are left behind or skipped.

However, enabling catchup can also cause a flood of task executions, which may overload your system or cause other issues. Therefore, it is important to use this feature judiciously and consider the potential impact before enabling it.

```python
from airflow.models import DAG
from datetime import datetime, timedelta

default_args = {
    'owner': 'Pratik',
    'depends_on_past': False,
    'start_date': datetime(2023, 4, 1),
    'retries': 0
}

dag = DAG(
    'example_dag',
    default_args=default_args,
    description='Example DAG',
    schedule_interval='@daily',
    catchup=True # Enable catch up
)

# Define your tasks here...
```

> Note: By default, `catchup` is set to true
> 

**Backfill**

We can achieve the same thing mentioned using `backfill` above if we `catchup` was set to false

"Backfill" in Apache Airflow refers to the process of scheduling and running tasks for a specific date range in the past. This can be useful when you want to re-run tasks that failed, or when you need to update the output of a task based on updated data.

Backfilling in Airflow can be performed using the **`backfill`** command-line tool or the **`BackfillJob`** class in the Airflow API. When running a backfill job, Airflow will execute all the tasks in the DAG for the specified date range, taking into account any dependencies and retries.

Here's an example of how you can run a backfill job using the Airflow CLI:

```bash
#Syntex airflow backfill dag_id -s startdate -e enddate
airflow backfill example_dag -s 2023-03-01 -e 2023-03-05
```

In the command above, we're running a backfill job for the "example_dag" DAG, starting from March 1st, 2023, and ending on March 5th, 2023. Airflow will execute all the tasks in the DAG for each of the specified dates, retrying any failed tasks according to the DAG's retry settings.

Note that backfilling can be resource-intensive, especially if you're backfilling a large number of dates or if your DAG has many dependencies. Therefore, it's important to carefully consider the potential impact on your system before running a backfill job.

### Scheduler with CRON expression

While we are creating DAG we have to specify `schedule_interval` parameter value of this could be `datetime.timedelta` or `CRON` expression 

> Note: `@hourely` `@daily` are the presets provided by Airflow this is also linked to CRON expressions
> 

A CRON expression consists of five or six fields, separated by spaces, that represent different time components. Here's the general format:

```

*    *    *    *    *    *
┬    ┬    ┬    ┬    ┬    ┬
│    │    │    │    │    │
│    │    │    │    │    └─ Year (optional)
│    │    │    │    └───── Day of week (0 - 7) (Sunday is 0 or 7)
│    │    │    └────────── Month (1 - 12)
│    │    └─────────────── Day of month (1 - 31)
│    └──────────────────── Hour (0 - 23)
└───────────────────────── Minute (0 - 59)

```

The fields are interpreted as follows:

- Minute: 0-59
- Hour: 0-23
- Day of month: 1-31
- Month: 1-12
- Day of week: 0-7 (both 0 and 7 represent Sunday)

An asterisk **`*`** in a field means "any value". For example, **`* * * * *`** means "run the task every minute, every hour, every day, every month, and every day of the week".

You can also use specific values, ranges, and intervals in each field. For example:

- **`0 6 * * *`**: Run the task at 6:00 AM every day.
- **`0 0 * * 0`**: Run the task at midnight on Sundays.
- **`0 */2 * * *`**: Run the task every two hours.
- **`0 0 1-15 * *`**: Run the task at midnight on the first 15 days of every month.
- `**0 3 * * Tue-Fri**`: Run task at 3:00 every day of the week from Tuesday to Friday
- `**0 3 * * Tue,Fri**`: Run task at 3:00 every day of the week from Tuesday & Friday

There are many other possibilities with CRON expressions, including the ability to use special characters like **`/`**, **`-`**, and **`,`**. It's important to carefully read the documentation for your system or job scheduler to understand the full range of options available with CRON expressions.

To build CRON expressions visually follow use this website

[Crontab.guru - The cron schedule expression editor](https://crontab.guru/)

### Airflow Connections

In Airflow, a Connection is a representation of a specific external system or service that your DAGs need to interact with, such as a database, a cloud storage provider, or an API endpoint.

A Connection defines the necessary information for Airflow to connect to that system, such as the hostname, port number, login credentials, and other configuration details.

By defining Connections in Airflow, you can **centralize and manage all the necessary information for your DAGs** to interact with external systems and services, instead of hardcoding these details into your DAG code.

Once you define a Connection in Airflow, you can use it in your DAG tasks to connect to the external system or service, without exposing sensitive information in your code.
