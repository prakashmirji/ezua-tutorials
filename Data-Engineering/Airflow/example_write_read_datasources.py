from airflow import DAG
from airflow.decorators import task
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0
}

with DAG(
        'files_transfer',
        default_args=default_args,
        schedule_interval=None,
        tags=['DF']
) as dag:
    file_path = "/mnt/datasources/df/test.txt"


    @task
    def write():
        with open(file_path, 'w') as fp:
            print("=====>>>  Started writing")
            fp.write("Hello world")
            print("=====>>>  Writing complete")


    @task
    def read():
        with open(file_path) as fp:
            print("=====>>> Content is: " + fp.read())


    write() >> read()
