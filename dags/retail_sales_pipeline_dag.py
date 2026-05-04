from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime

default_args = {
    "start_date": datetime(2024, 1, 1)
}

with DAG(
    dag_id="retail_sales_pipeline",
    schedule=None,
    default_args=default_args,
    catchup=False
) as dag:

    silver_task = BashOperator(
        task_id="silver_transformation",
        bash_command="""
        spark-submit /home/pacific/projects/retail-sales-cloud-pipeline/pyspark/jobs/silver/silver_transformation.py
        """
    )

    gold_task = BashOperator(
        task_id="gold_kpi_aggregation",
        bash_command="""
        spark-submit /home/pacific/projects/retail-sales-cloud-pipeline/pyspark/jobs/gold/gold_kpi_aggregation.py
        """
    )

    silver_task >> gold_task