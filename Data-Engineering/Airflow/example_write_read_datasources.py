from airflow import DAG
from airflow.models.param import Param
from airflow.decorators import task
from airflow.utils.dates import days_ago
from airflow.operators.python import get_current_context


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'max_active_runs': 1,
    'retries': 0
}

with DAG(
        'write_read_file_external_df',
        default_args=default_args,
        schedule_interval=None,
        tags=['ezaf', 'external DF'],
        params={
            'file_path': Param("/mnt/datasources/df/airflow_write_read_test.txt", type="string"),
        },
        render_template_as_native_obj=True,
        access_control={
            'All': {
                'can_read',
                'can_edit',
                'can_delete'
            }
        }
) as dag:

    @task
    def write():
        file_path = get_current_context()['params']['file_path']

        with open(file_path, 'w') as fp:
            print("Started writing file: ", file_path)
            fp.write("This this test message to verify writing and reading file to External DF by Airflow DAG.")
            print("Writing complete")

    @task
    def read():
        file_path = get_current_context()['params']['file_path']

        with open(file_path) as fp:
            print("Start reading file: ", file_path)
            print("Content of the file is: ", fp.read())
            print("Reading complete")


    write() >> read()
