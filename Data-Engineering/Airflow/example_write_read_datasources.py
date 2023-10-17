from airflow import DAG
from airflow.models.param import Param
from airflow.decorators import task
from airflow.utils.dates import days_ago
import logging

logger = logging.getLogger(__name__)

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
        }
) as dag:
    file_path = "{{dag_run.conf['file_path', '/mnt/datasources/df/airflow_write_read_test.txt']}}"


    @task
    def write():
        with open(file_path, 'w') as fp:
            logger.info("Started writing file: ", file_path)
            fp.write("This this test message to verify writing and reading file to External DF by Airflow DAG.")
            logger.info("Writing complete")


    @task
    def read():
        with open(file_path) as fp:
            logger.info("Start reading file: ", file_path)
            logger.info("Content of the file is: ", fp.read())
            logger.info("Reading complete")


    write() >> read()
